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
    # url/createDatabase?dbname=<dbname>
    database_name = request.args.get("dbname")
    connection = psycopg2.connect("host='localhost' user=postgres password=test")
    database_creation_sql = "create database " + database_name + ";"
    connection.autocommit = True
    try:
        with connection.cursor() as cursor:
            cursor.execute(database_creation_sql)
            return "Database created Successfully"
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
