import csv
# import novaclient
# from novaclient import client
import os
import schedule

# import psycopg2
# from psycopg2.extras import LogicalReplicationConnection
import time
import atexit
from apscheduler.schedulers.background import BackgroundScheduler

header = ['ID', 'VM', 'IsAlive', 'Space']


def update_central_repo():
    print("yolo")
    with open('central_repository.csv', 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)

        # HOST_UP = False if os.system("ping -c 1 " + "10.0.0.220") != 0 else True
        # HOST_UP = False if os.system("ping -c 1 " + "10.0.0.125") != 0 else True
        # HOST_UP = False if os.system("ping -c 1 " + "192.168.100.66") != 0 else True
        # HOST_UP = False if os.system("ping -c 1 " + "10.0.0.17") != 0 else True
        # print(HOST_UP)

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
            row = {'ID': i + 1, 'VM': ip, 'IsAlive': HOST_UP, 'Space': "unknown"}
            writer.writerow(row)

    with open('central_repository.csv', 'r', encoding='UTF8', newline='') as f:
        readData = [row for row in csv.reader(f)]
        print(readData)

schedule.every(15).seconds.do(update_central_repo)

while True:
    # Checks whether a scheduled task
    # is pending to run or not
    schedule.run_pending()
    time.sleep(1)

# scheduler = BackgroundScheduler(timezone="America/New_York")
# scheduler.add_job(func=update_central_repo, trigger="interval", seconds=15)
# scheduler.start()
#
# # Shut down the scheduler when exiting the app
# atexit.register(lambda: scheduler.shutdown())

# for instance in client.
#    print(instance.name)
#    print(instance.addresses)
#    print(instance.status)
