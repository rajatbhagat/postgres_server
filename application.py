# Importing flask module in the project is mandatory
# An object of Flask class is our WSGI application.
import sys
from flask import Flask
from client.client_blueprint import client_blueprint
from postgres_instance.instance_blueprint import instance_blueprint
from server.server_blueprint import server_blueprint
from postgres_database.database_blueprint import database_blueprint
from util.blueprint_config import CLIENT_API_URL_PREFIX, SERVER_API_URL_PREFIX, \
    INSTANCE_API_URL_PREFIX, DATABASE_API_URL_PREFIX

# Flask constructor takes the name of
# current module (__name__) as argument.
app = Flask(__name__)

# Collection of the blueprints that need to be registered with the Flask App.
client_jobs = [
    (client_blueprint, CLIENT_API_URL_PREFIX),
    (instance_blueprint, INSTANCE_API_URL_PREFIX)
]

server_jobs = [
    (instance_blueprint, INSTANCE_API_URL_PREFIX),
    (server_blueprint, SERVER_API_URL_PREFIX),
    (database_blueprint, DATABASE_API_URL_PREFIX)
]

instance_type = sys.argv[0]
blueprint_to_be_loaded = []
if instance_type == "client":
    blueprint_to_be_loaded = client_jobs
else:
    blueprint_to_be_loaded = server_jobs

# Registering the different blueprints with the flask app.

if instance_type == "" or instance_type is None:
    blueprint_to_be_loaded = client_jobs

for blueprint_option, prefix in blueprint_to_be_loaded:
    app.register_blueprint(blueprint_option, url_prefix=prefix)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
