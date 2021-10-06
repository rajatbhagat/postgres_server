from flask import Blueprint

client_blueprint = Blueprint("client_blueprint", __name__)


@client_blueprint.route("/")
def index():
    return "Default client api call"


@client_blueprint.route("/databaseDetails")
def get_database_details():
    return "This call will give us the database details"


@client_blueprint.route("/getDatabaseInstanceDetails")
def get_database_instance_details():
    return "This call will get the database instance details"


@client_blueprint.route("/getAvailablSpaceInVm")
def get_available_space_in_vm():
    return "This call will hit the central repo and get the details of the VM that has space"


