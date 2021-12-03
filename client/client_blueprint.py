from flask import Blueprint
from flask_restx import Api, Resource

client_blueprint = Blueprint("client_blueprint", __name__)
client_api = Api(client_blueprint)

client_namespcae = client_api.namespace("client");

@client_namespcae.route("/")
class ClientIndex(Resource):
    def get(self):
        return "Default client api call"


@client_namespcae.route("/databaseDetails")
class DatabaseDetails(Resource):
    def get(self):
        return "This call will give us the database details"


@client_namespcae.route("/getConnectionString")
class ConnectionString(Resource):
    def get(self):
        return "This call will give us the connection string to connect to a database"


@client_namespcae.route("/getDatabaseInstanceDetails")
class DatabaseInstanceDetails(Resource):
    def get_database_instance_details(self):
        return "This call will get the database instance details"


@client_namespcae.route("/getAvailablSpaceInVm")
class AvailablSpaceInVM(Resource):
    def get(self):
        return "This call will hit the central repo and get the details of the VM that has space"


@client_namespcae.route("/updateCentralDatabase")
class UpdateCentralRepository(Resource):
    def get(self):
        return "This call will update the central database."