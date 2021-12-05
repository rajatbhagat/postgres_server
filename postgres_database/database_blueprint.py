from flask import Blueprint
import psycopg2
from flask_restx import Api, Resource

from util.utils import add_entry_to_db_repo, update_active_flag_db_repo, check_db_exists

database_blueprint = Blueprint("database_blueprint", __name__)
database_api = Api(database_blueprint)

database_namespace = database_api.namespace("database")


@database_namespace.route("/createDatabase/<string:dbname>&<string:uname>")
class CreateDatabase(Resource):
    def post(self, dbname, uname):
        # url/createDatabase?dbname=<dbname>&uname=<username>
        # database_name = request.args.get("dbname")
        # user_name = request.args.get("uname")
        database_name = dbname
        user_name = uname
        if check_db_exists(dbname, user_name):
            return "Database with " + dbname + "exists."
        connection = psycopg2.connect("host='localhost' user=postgres password=test")
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
        connection = psycopg2.connect("host='localhost' user=postgres password=test")
        database_creation_sql = "create database " + database_name + " owner " + user_name + ";"
        revoke_privileges_for_public = "revoke connect on database " + database_name + " from public"
        connection.autocommit = True
        try:
            with connection.cursor() as cursor:
                cursor.execute(database_creation_sql)
                cursor.execute(revoke_privileges_for_public)
                # connection.commit()
                add_entry_to_db_repo(database_name, "128.31.27.249", user_name, 'Active', 'RW')
                return {"host": "128.31.27.249", "port": 5432, "database": database_name, "username": user_name,
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
            connection = psycopg2.connect(host='localhost', dbname=database_name, user=user_name, password=pwd)
        except Exception as e:
            return "connection failed" + e.__str__()
        return "connection established"


@database_namespace.route("/dropDatabase/<string:dbname>")
class DropDatabase(Resource):
    def post(self, dbname):
        # database_name = request.args.get("dbname")
        database_name = dbname
        connection = psycopg2.connect("host='localhost' user=postgres password=test")
        connection.autocommit = True
        database_deletion_sql = "drop database " + database_name + ";"
        try:
            with connection.cursor() as cursor:
                cursor.execute(database_deletion_sql)
                update_active_flag_db_repo(dbname, 'Inactive')
                return "Database dropped Successfully"
        except Exception as e:
            return "Exception while dropping database : " + e.__str__()


@database_namespace.route("/dropDatabaseByOwner/<string:dbname>&<string:uname>&<string:pwd>")
# url/dropDatabaseByOwner?dbname=<dbname>&uname=<username>&pwd=<pwd>
class DropDatabaseByOwner(Resource):
    def post(self, dbname, uname, pwd):
        # database_name = request.args.get("dbname")
        # user_name = request.args.get("uname")
        # pwd = request.args.get("pwd")
        database_name = dbname
        user_name = uname
        pwd = pwd
        res = verify_user(database_name, user_name, pwd)
        if res != "success":
            return "Can not verify user credentials to the database"
        connection = psycopg2.connect("host='localhost' user=postgres password=test")
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


def verify_user(database_name, user_name, pwd):
    conn_str = "host='localhost' user=" + user_name + " password=" + pwd + " dbname=" + database_name
    try:
        connection = psycopg2.connect(conn_str)
        connection.close()
        return "success"
    except Exception as e:
        return "Exception while verify user credentials" + e.__str__()


@database_namespace.route("/accessDB/<string:dbname>&<string:uname>&<string:pwd>")
# url/accessDB?dbname=<dbname>&uname=<username>&pwd=<pwd>
class AccessDatabase(Resource):
    def post(self, dbname, uname, pwd):
        # database_name = request.args.get("dbname")
        # user_name = request.args.get("uname")
        # pwd = request.args.get("pwd")
        database_name = dbname
        user_name = uname
        pwd = pwd
        res = verify_user(database_name, user_name, pwd)
        return {"res": res, "host": "128.31.27.249", "port": 5432, "database": database_name, "username": user_name,
                "password": pwd}


@database_namespace.route("/modifySettings")
class ModifyDatabaseSettings(Resource):
    def post(self):
        return "This call will help the user modify the settings of the database."


@database_namespace.route("/getSize/<string:dbname>")
class GetDatabaseSize(Resource):
    def get(self, dbname):
        # url/getSize?dbname=<dbname>
        # database_name = request.args.get("dbname")
        database_name = dbname
        connection = psycopg2.connect("host='localhost' user=postgres password=test")
        database_size_sql = "SELECT pg_size_pretty( pg_database_size('" + database_name + "') );"
        connection.autocommit = True
        try:
            with connection.cursor() as cursor:
                cursor.execute(database_size_sql)
                row = cursor.fetchone()
                return str(row[0])
        except Exception as e:
            return "Exception while getting database size: " + e.__str__()


@database_namespace.route("/getStats/<string:dbname>")
class GetDatabaseStats(Resource):
    def get(self, dbname):
        # url/getStats?dbname=<dbname>
        # database_name = request.args.get("dbname")
        database_name = dbname
        connection = psycopg2.connect("host='localhost' user=postgres password=test")
        database_size_sql = "SELECT * FROM pg_stat_database WHERE datname = '" + database_name + "';"
        connection.autocommit = True
        try:
            with connection.cursor() as cursor:
                cursor.execute(database_size_sql)
                row = cursor.fetchall()
                return str(row)
        except Exception as e:
            return "Exception while getting database size: " + e.__str__()


@database_namespace.route("/updateReadStatus/<string:dbname>&<string:uname>")
class UpdateReadAccess(Resource):
    def post(self, dbname, uname):
        # url/createDatabase?dbname=<dbname>&uname=<username>
        # database_name = request.args.get("dbname")
        # user_name = request.args.get("uname")
        database_name = dbname
        user_name = uname
        connection = psycopg2.connect("host='localhost' user=postgres password=test")
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
            connection = psycopg2.connect("host='localhost' user=postgres password=test")
            grant_connect_and_read_to_user = "grant connect on database " + database_name + " to " + user_name + ";"
            # connection.autocommit = True
            try:
                with connection.cursor() as cursor:
                    cursor.execute(grant_connect_and_read_to_user)
                    connection.commit()
                    return {"host": "128.31.27.249", "port": 5432, "database": database_name, "username": user_name,
                            "password": "dummy_pwd#1234"}
            except Exception as e:
                return "Exception while creating database : " + e.__str__()
