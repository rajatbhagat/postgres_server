# Importing flask module in the project is mandatory
# An object of Flask class is our WSGI application.
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
blueprint = [
    (client_blueprint, CLIENT_API_URL_PREFIX),
    (instance_blueprint, INSTANCE_API_URL_PREFIX),
    (server_blueprint, SERVER_API_URL_PREFIX),
    (database_blueprint, DATABASE_API_URL_PREFIX)
]

# Registering the different blueprinst with the flask app.
for blueprint, prefix in blueprint:
    app.register_blueprint(blueprint, url_prefix=prefix)

app.run()
