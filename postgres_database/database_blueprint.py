from flask import Blueprint
from flask import request
import psycopg2

database_blueprint = Blueprint("database_blueprint", __name__)


@database_blueprint.route("/")
def database_index():
    # return request.args.get("dbname")
    return "Default route for database."


@database_blueprint.route("/createDatabase")
def create_database():
    # url/createDatabase?dbname=<dbname>&uname=<username>
    database_name = request.args.get("dbname")
    user_name = request.args.get("uname")
    connection = psycopg2.connect("host='localhost' user=postgres password=test")
    check_user_exists_query = "select 1 from pg_roles where pg_roles.rolname='" + user_name + "';"
    with connection.cursor() as cursor:
        user_exists = cursor.execute(check_user_exists_query)
        if not user_exists:
            create_user_query = "create user " + user_name + " with password " + "'dummy_pwd#1234';"
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
            return {"host": "128.31.27.249", "port": 5432, "database": database_name, "username": user_name, "password": "dummy_pwd#1234"}
    except Exception as e:
        return "Exception while creating database : " + e.__str__()


@database_blueprint.route("/dropDatabase")
def drop_database():
    # url/dropDatabase?dbname=<dbname>
    database_name = request.args.get("dbname")
    connection = psycopg2.connect("host='localhost' user=postgres password=test")
    connection.autocommit = True
    database_deletion_sql = "drop database " + database_name + ";"
    try:
        with connection.cursor() as cursor:
            cursor.execute(database_deletion_sql)
            return "Database dropped Successfully"
    except Exception as e:
        return "Exception while dropping database : " + e.__str__()


@database_blueprint.route("/modifySettings")
def modify_database_settings():
    return "This call will help the user modify the settings of the database."
