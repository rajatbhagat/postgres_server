#!/usr/bin/env python3
import psycopg2
from time import sleep
import requests
import socket

URL="http://128.31.25.198:5000/client/client/updateCentralDatabasePoller"
PORT=5000
INTERVAL=3.0
CONN_STR = "host=localhost user=postgres password=postgres"

def get_ip():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        try:
            sock.connect(("8.8.8.8", 80))
            return sock.getsockname()[0]
        except:
            return "error"

def get_type():
    conn = psycopg2.connect(CONN_STR)
    cur = conn.cursor()
    cur.execute("SELECT pg_is_in_recovery();")
    result= cur.fetchall()[0][0]
    if result is False:
        conn.close()
        return "master"
    elif result is True:
        conn.close()
        return "slave"
    conn.close()
    return "error"
    

if __name__ == "__main__":
    ip = get_ip()
    while True:
        type=get_type()
        data={'type':type, 'ip':ip}
        res = requests.post(URL, json=data)
        print(res)
        sleep(INTERVAL)
