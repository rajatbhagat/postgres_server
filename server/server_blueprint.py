from flask import Blueprint
from flask_restx import Api, Resource

server_blueprint = Blueprint("server_blueprint", __name__)
server_api = Api(server_blueprint)

server_namespace = server_api.namespace("server")


@server_namespace.route("/")
class ServerIndex(Resource):
    @server_namespace.doc("get")
    def get(self):
        return "This is the default call for the server API."


@server_namespace.route("/updateCentralDatabase")
class UpdateCentralDB(Resource):
    def get(self, id, name):
        return "This call will be used to update the central database." + id + name
