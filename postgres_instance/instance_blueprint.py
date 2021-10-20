from flask import Blueprint

instance_blueprint = Blueprint("instance_blueprint", __name__)


@instance_blueprint.route("/")
def instance_index():
    return "Default call for the instance apis"


@instance_blueprint.route("/createInstance")
def create_instance():
    return "This call will create an instance."


@instance_blueprint.route("/getInstanceDetails")
def get_instance_details():
    return "This call will get the details of the instance."


@instance_blueprint.route("/modifyInstanceSettings")
def modify_instance_details():
    return "This call will modify the instance settings."
