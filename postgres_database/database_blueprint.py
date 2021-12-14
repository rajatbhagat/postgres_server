from flask import Blueprint, request
import psycopg2
from flask_restx import Api, Resource, reqparse

from util.utils import add_entry_to_db_repo, update_active_flag_db_repo, check_db_exists, get_vm_details, \
    check_available_space

database_blueprint = Blueprint("database_blueprint", __name__)
database_api = Api(database_blueprint)

database_namespace = database_api.namespace("database")

# Define parser and request args
parser = reqparse.RequestParser()
parser.add_argument('dbname', type=str, required=True, location='json')
parser.add_argument('uname', type=str, required=True, location='json')
parser.add_argument('pwd', type=str, required=False, location='json')
args = parser.args


@database_namespace.route("/createDatabase")
# /createDatabase/<string:dbname>&<string:uname>
class CreateDatabase(Resource):
    @database_namespace.expect(parser)
    def post(self):
        # url/createDatabase?dbname=<dbname>&uname=<username>
        # database_name = request.json['dbname']
        # user_name = request.json['uname']
        database_name = parser.parse_args()["dbname"]
        user_name = parser.parse_args()["uname"]
        if check_db_exists(database_name, user_name):
            return "Database with " + database_name + "exists."
        host = check_available_space()
        connection = psycopg2.connect('host='+host+' user=postgres password=postgres')
        check_user_exists_query = "select 1 from pg_roles where pg_roles.rolname='" + user_name + "';"
        with connection.cursor() as cursor:
            user_exists = cursor.execute(check_user_exists_query)
            record = cursor.fetchall()
            print(record)
            if not record:
                create_user_query = "create user " + user_name + " with password " + "'dummy_pwd1234';"
                cursor.execute(create_user_query)
                connection.commit()
        connection.close()
        connection = psycopg2.connect('host='+host+' user=postgres password=postgres')
        database_creation_sql = "create database " + database_name + " owner " + user_name + ";"
        revoke_privileges_for_public = "revoke connect on database " + database_name + " from public"
        connection.autocommit = True
        try:
            with connection.cursor() as cursor:
                cursor.execute(database_creation_sql)
                cursor.execute(revoke_privileges_for_public)
                # connection.commit()
                add_entry_to_db_repo(database_name, host, user_name, 'Active', 'RW')
                return {"host": host, "port": 5432, "database": database_name, "username": user_name,
                        "password": "dummy_pwd1234"}
        except Exception as e:
            return "Exception while creating database : " + e.__str__()


# not committed yet
@database_namespace.route("/connectDB/<string:dbname>&<string:uname>&<string:pwd>")
class ConnectDB(Resource):
    def get(self, dbname, uname, pwd):
        # database_name = request.args.get("dbname")
        # user_name = request.args.get("uname")
        # pwd = request.args.get("pwd")
        database_name = dbname
        user_name = uname
        pwd = pwd
        try:
            db_vm = get_vm_details(database_name)
            if db_vm is not None:
                connection = psycopg2.connect(host=db_vm, dbname=database_name, user=user_name, password=pwd)
        except Exception as e:
            return "connection failed" + e.__str__()
        return "connection established"


@database_namespace.route("/dropDatabase")
# /dropDatabase/<string:dbname>
class DropDatabase(Resource):
    @database_namespace.expect(parser)
    def post(self):
        # database_name = request.args.get("dbname")
        #database_name = dbname
        database_name = parser.parse_args()["dbname"]
        # database_name = request.json['dbname']
        db_vm = get_vm_details(database_name)
        if db_vm is not None:
            connection = psycopg2.connect("host='"+ db_vm + "' user=postgres password=test")
            connection.autocommit = True
            database_deletion_sql = "drop database " + database_name + ";"
            try:
                with connection.cursor() as cursor:
                    cursor.execute(database_deletion_sql)
                    update_active_flag_db_repo(database_name, 'Inactive')
                    return "Database dropped Successfully"
            except Exception as e:
                return "Exception while dropping database : " + e.__str__()
        return "No database found"


@database_namespace.route("/dropDatabaseByOwner")
# url/dropDatabaseByOwner?dbname=<dbname>&uname=<username>&pwd=<pwd>
# "/dropDatabaseByOwner/<string:dbname>&<string:uname>&<string:pwd>"
class DropDatabaseByOwner(Resource):
    @database_namespace.expect(parser)
    def post(self):
        # database_name = request.args.get("dbname")
        # user_name = request.args.get("uname")
        # pwd = request.args.get("pwd")
        # database_name = request.json['dbname']
        # user_name = request.json['uname']
        # pwd = request.json['pwd']
        database_name = parser.parse_args()["dbname"]
        user_name = parser.parse_args()["uname"]
        pwd = parser.parse_args()['pwd']
        res = verify_user(database_name, user_name, pwd)
        if res != "success":
            return "Can not verify user credentials to the database"
        db_vm = get_vm_details(database_name)
        if db_vm is not None:
            connection = psycopg2.connect("host='"+ db_vm +"' user=postgres password=postgres")
            connection.autocommit = True
            # collect db owner information
            check_db_owner_query = 'SELECT d.datname as "Name", pg_catalog.pg_get_userbyid(d.datdba) as "Owner" FROM pg_catalog.pg_database d WHERE d.datname = ' + "'" + database_name + "'" + ' ORDER BY 1;'
            owners = []
            try:
                with connection.cursor() as cursor:
                    cursor.execute(check_db_owner_query)
                    record = cursor.fetchall()
                    for n in record:
                        owners.append(n)
            except Exception as e:
                return "Exception while getting owner information of a db: " + e.__str__()

            # if username match db owner, drop db
            for row in owners:
                owner = row[1]
                if user_name == owner:
                    database_deletion_sql = "drop database " + database_name + ";"
                    try:
                        with connection.cursor() as cursor:
                            cursor.execute(database_deletion_sql)
                            return "Database dropped Successfully"
                    except Exception as e:
                        return "Exception while dropping database : " + e.__str__()
            connection.close()
            return "user is not the database owner"
        return "No Database found"


def verify_user(database_name, user_name, pwd):
    db_vm = get_vm_details(database_name)
    if db_vm is not None:
        conn_str = "host='"+db_vm+"' user=" + user_name + " password=" + pwd + " dbname=" + database_name
        try:
            connection = psycopg2.connect(conn_str)
            connection.close()
            return "success"
        except Exception as e:
            return "Exception while verify user credentials" + e.__str__()
    else:
        return None


@database_namespace.route("/accessDB")
# /accessDB/<string:dbname>&<string:uname>&<string:pwd>
# url/accessDB?dbname=<dbname>&uname=<username>&pwd=<pwd>
class AccessDatabase(Resource):
    @database_namespace.expect(parser)
    def post(self):
        # database_name = request.args.get("dbname")
        # user_name = request.args.get("uname")
        # pwd = request.args.get("pwd")
        # database_name = request.json['dbname']
        # user_name = request.json['uname']
        # pwd = request.json['pwd']
        database_name = parser.parse_args()["dbname"]
        user_name = parser.parse_args()["uname"]
        pwd = parser.parse_args()['pwd']
        res = verify_user(database_name, user_name, pwd)
        if res == "success":
            return {"res": res, "host": "128.31.27.249", "port": 5432, "database": database_name, "username": user_name,
                    "password": pwd}
        else:
            return {"res": "error", "host": "error", "port": "error", "database": "error", "username": "error",
                    "password": "error"}


@database_namespace.route("/getSize/<string:dbname>")
class GetDatabaseSize(Resource):
    def get(self, dbname):
        # url/getSize?dbname=<dbname>
        # database_name = request.args.get("dbname")
        database_name = dbname
        db_vm = get_vm_details(database_name)
        if db_vm is not None:
            connection = psycopg2.connect("host='" + db_vm + "' user=postgres password=postgres")
            database_size_sql = "SELECT pg_size_pretty( pg_database_size('" + database_name + "') );"
            connection.autocommit = True
            try:
                with connection.cursor() as cursor:
                    cursor.execute(database_size_sql)
                    row = cursor.fetchone()
                    return str(row[0])
            except Exception as e:
                return "Exception while getting database size: " + e.__str__()
        else:
            return "Database Not found"


@database_namespace.route("/getStats/<string:dbname>")
class GetDatabaseStats(Resource):
    def get(self, dbname):
        # url/getStats?dbname=<dbname>
        # database_name = request.args.get("dbname")
        database_name = dbname
        db_vm = get_vm_details(database_name)
        if db_vm is not None:
            connection = psycopg2.connect("host='"+db_vm+"' user=postgres password=postgres")
            database_size_sql = "SELECT * FROM pg_stat_database WHERE datname = '" + database_name + "';"
            connection.autocommit = True
            try:
                with connection.cursor() as cursor:
                    cursor.execute(database_size_sql)
                    row = cursor.fetchall()
                    return str(row)
            except Exception as e:
                return "Exception while getting database size: " + e.__str__()
        return "Database not found"


@database_namespace.route("/updateReadStatus")
# /updateReadStatus/<string:dbname>&<string:uname>
class UpdateReadAccess(Resource):
    @database_namespace.expect(parser)
    def post(self):
        # url/createDatabase?dbname=<dbname>&uname=<username>
        # database_name = request.args.get("dbname")
        # user_name = request.args.get("uname")
        # database_name = request.json['dbname']
        # user_name = request.json['uname']
        database_name = parser.parse_args()["dbname"]
        user_name = parser.parse_args()["uname"]
        # pwd = parser.parse_args()['pwd']
        db_vm = get_vm_details(database_name)
        if db_vm is not None:
            connection = psycopg2.connect("host='"+db_vm+"' user=postgres password=postgres")
            check_user_exists_query = "select 1 from pg_roles where pg_roles.rolname='" + user_name + "';"
            with connection.cursor() as cursor:
                cursor.execute(check_user_exists_query)
                record = cursor.fetchall()
                print(record)
                if not record:
                    create_user_query = "create user " + user_name + " with password " + "'dummy_pwd#1234';"
                    cursor.execute(create_user_query)
                    connection.commit()
                connection.close()
                connection = psycopg2.connect("host='"+db_vm+"' user=postgres password=postgres")
                grant_connect_and_read_to_user = "grant connect on database " + database_name + " to " + user_name + ";"
                # connection.autocommit = True
                try:
                    with connection.cursor() as cursor:
                        cursor.execute(grant_connect_and_read_to_user)
                        connection.commit()
                        return {"host": db_vm, "port": 5432, "database": database_name, "username": user_name,
                                "password": "dummy_pwd#1234"}
                except Exception as e:
                    return "Exception while creating database : " + e.__str__()
        return "Database not found"
