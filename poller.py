#!/usr/bin/env python3
import psycopg2
from time import sleep
import requests
import socket
import sys

#SERVER_IP="128.31.25.198"
URL="http://128.31.25.198:5000/client/client/updateCentralDatabasePoller"
PORT=5000
ID=1
INTERVAL=3.0
type = "slave"

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
    try:
        sock.connect(("8.8.8.8", 80))
        ip = sock.getsockname()[0]
    except:
        print("Could not detect local IP. Exiting.")
        sys.exit(1)
# data={'type':type, 'ip':ip}

conn_str = "host=localhost user=postgres password=postgres"

while True:
    conn = psycopg2.connect(conn_str)
    cur = conn.cursor()
    cur.execute("SELECT pg_is_in_recovery();")
    result= cur.fetchall()[0][0]
    if result is False:
        type="master"
    conn.close()
    #print(type)
    data={'type':type, 'ip':ip, 'id':ID}
    res = requests.post(URL, json=data)
    print(res)
    sleep(INTERVAL)
