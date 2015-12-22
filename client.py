import threading, time
import socket

class Client(threading.Thread):
    def __init__(self, ip):
        print "Connecting to: " + ip
        
    def run(self):
        while True:
            time.sleep(100)

        print "Client Ran"
