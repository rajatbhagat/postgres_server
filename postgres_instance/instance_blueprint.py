from flask import Blueprint
from flask_restx import Api, Resource

instance_blueprint = Blueprint("instance_blueprint", __name__)
instance_api = Api(instance_blueprint)

instance_namespace = instance_api.namespace("instance")


@instance_namespace.route("/")
class InstanceBasic(Resource):
    def get(self):
        return "Default call for the instance apis"


@instance_namespace.route("/createInstance")
class CreateInstanceBasic(Resource):
    def get(self):
        return "This call will create an instance."


@instance_namespace.route("/getInstanceDetails")
class InstanceDetails(Resource):
    def get(self):
        return "This call will get the details of the instance."


@instance_namespace.route("/modifyInstanceSettings")
class ModifyInstanceDetails(Resource):
    def get(self):
        return "This call will modify the instance settings."
