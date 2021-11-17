import csv
import novaclient
header = ['VM', 'IsAlive', 'Space']
# import psycopg2
# from psycopg2.extras import LogicalReplicationConnection

with open('central_repository.csv', 'w', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(header)
for instance in novaclient.servers.list():
    print(instance.name)
    print(instance.addresses)
    print(instance.status)
