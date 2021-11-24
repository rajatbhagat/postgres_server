from flask import Blueprint

client_blueprint = Blueprint("client_blueprint", __name__)
import csv
import os

@client_blueprint.route("/")
def index():
    return "Default client api call"


@client_blueprint.route("/databaseDetails")
def get_database_details():
    return "This call will give us the database details"


@client_blueprint.route("/getConnectionString")
def get_connection_string(database_name):
    return "This call will give us the connection string to connect to a database"


@client_blueprint.route("/getDatabaseInstanceDetails")
def get_database_instance_details():
    return "This call will get the database instance details"


@client_blueprint.route("/getAvailablSpaceInVm")
def get_available_space_in_vm():
    return "This call will hit the central repo and get the details of the VM that has space"


@client_blueprint.route("/updateCentralDatabase")
def update_central_database():
    with open('central_repository.csv', 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
    header = ['ID', 'VM', 'IsAlive', 'Space']
    writer = csv.DictWriter(f, fieldnames=header)
    for i in range(4):
        if i == 0:
            ip = "10.0.0.220"
        elif i == 1:
            ip = "10.0.0.125"
        elif i == 2:
            ip = "192.168.100.66"
        elif i ==3:
            ip = "10.0.0.17"
        HOST_UP = False if os.system("ping -c 1 " + ip) != 0 else True
        row = {'ID': i + 1, 'IsAlive': HOST_UP, 'Space': "unknown"}
        writer.writerow(row)
    return "This call will update the central database."

@client_blueprint.route("/getcsv")
def get_csv():
    return "This call will hit the central repo and get the details of the VM that has space"


