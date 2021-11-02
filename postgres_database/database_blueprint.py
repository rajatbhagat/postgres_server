from flask import Blueprint
from flask import request
import psycopg2
from psycopg2.extras import LogicalReplicationConnection

database_blueprint = Blueprint("database_blueprint", __name__)


@database_blueprint.route("/")
def database_index():
    return "Default route for database."


@database_blueprint.route("/createDatabase")
def create_database():
    database_name = request.args.get("dbname")
    connection = psycopg2.connect("host='localhost' user=postgres password=test")
    database_creation_sql = "create database " + database_name + ";"
    try:
        with connection.cursor() as cursor:
            cursor.execute(database_creation_sql)
            return "Database created Successfully"
    except Exception as e:
        return "Exception while creating database : " + e.__str__()


@database_blueprint.route("/dropDatabase")
def drop_database():
    database_name = request.args.get("dbname")
    connection = psycopg2.connect("host='localhost' user=postgres password=test")
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

@database_blueprint.route("/getSize")
def get_database_size():
    # url/getSize?dbname=<dbname>
    database_name = request.args.get("dbname")
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


@database_blueprint.route("/getStats")
def get_database_stats():
    # url/getStats?dbname=<dbname>
    database_name = request.args.get("dbname")
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