import csv
# import novaclient
# from novaclient import client
import os
header = ['ID', 'VM', 'IsAlive', 'Space']
# import psycopg2
# from psycopg2.extras import LogicalReplicationConnection

with open('central_repository.csv', 'w', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(header)

HOST_UP = False if os.system("ping -c 1 " + "10.0.0.220") != 0 else True
HOST_UP = False if os.system("ping -c 1 " + "10.0.0.125") != 0 else True
HOST_UP = False if os.system("ping -c 1 " + "192.168.100.66") != 0 else True
HOST_UP = False if os.system("ping -c 1 " + "10.0.0.17") != 0 else True
print(HOST_UP)
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
    readData = [row for row in csv.DictReader(f)]
    print(readData)

#for instance in client.
#    print(instance.name)
#    print(instance.addresses)
#    print(instance.status)


