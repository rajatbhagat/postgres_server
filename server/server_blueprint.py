from flask import Blueprint

server_blueprint = Blueprint("server_blueprint", __name__)


@server_blueprint.route("/")
def index():
    return "This is the default call for the server API."


@server_blueprint.route("/updateCentralDatabase")
def update_central_database():
    return "This call will be used to update the central database."