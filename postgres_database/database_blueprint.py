from flask import Blueprint

database_blueprint = Blueprint("database_blueprint", __name__)


@database_blueprint.route("/")
def index():
    return "Default route for database."


@database_blueprint.route("/createDatabase")
def create_database():
    return "This call creates the database."


@database_blueprint.route("/dropDatabase")
def drop_database():
    return "This call will drop the database."


@database_blueprint.route("/modifySettings")
def modify_settings():
    return "This call will help the user modify the settings of the database."
