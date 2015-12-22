import threading
import socket
class Server(threading.Thread):
    def run(self):
        print "Players type this to join your server: " + socket.gethostbyname(socket.gethostname())
        while True:
            break

        print "Server Ran"
            
    
