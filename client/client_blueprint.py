from flask import Blueprint, request
from flask_restx import Api, Resource
import csv
import os
import pandas as pd

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


@client_namespcae.route("/getAvailableSpaceInVm")
class AvailableSpaceInVM(Resource):
    def get(self, VM):
        df = pd.read_csv('../central_repository.csv')
        if df.loc[df['VM'] == VM, 'IsAlive']:
            return df.loc[df['VM'] == VM, 'Space']
        else:
            return 'VM is not alive'
        # return "This call will hit the central repo and get the details of the VM that has space"

@client_namespcae.route("/updateCentralDatabasePoller")
class UpdateCentralRepositoryPoller(Resource):
    def post(self):
        id = request.json['id']
        ip = request.json['ip']
        type = request.json['type']
        res = "ip: " + ip + ", type: " + type
        print(res)
        with open('db_repository_poller.csv', 'w', encoding='UTF8', newline='') as f:
            writer = csv.writer(f)
            header = ['ID','VM', 'IsAlive', 'TYPE']
            writer = csv.DictWriter(f, fieldnames=header)
            HOST_UP = False if os.system("ping -c 1 " + ip) != 0 else True
            row = {'ID': int(id), 'VM': ip,'IsAlive': HOST_UP, 'TYPE':type}
            writer.writerow(row)
        return res


@client_namespcae.route("/updateCentralDatabase")
class UpdateCentralRepository(Resource):
    def post(self):
        with open('db_repository.csv', 'w', encoding='UTF8', newline='') as f:
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
            elif i == 3:
                ip = "10.0.0.17"
            HOST_UP = False if os.system("ping -c 1 " + ip) != 0 else True
            row = {'ID': i + 1, 'IsAlive': HOST_UP, 'Space': "unknown"}
            writer.writerow(row)
        return True


@client_blueprint.route("/getcsv")
def get_csv():
    return "This call will hit the central repo and get the details of the VM that has space"
