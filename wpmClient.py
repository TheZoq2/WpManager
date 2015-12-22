from multiprocessing import connection
import threading
import sys

REPLY_TIMEOUT = 0.5

def sendCommand(command):
    COMM_PORT = 6724

    address = ("localhost", COMM_PORT);

    conn = connection.Client(address)

    conn.send(command)

    #Wait for a reply
    if conn.poll(REPLY_TIMEOUT):
        print(conn.recv())

    conn.close()
