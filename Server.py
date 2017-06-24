import socket
import sys
from time import sleep

from User import User


class Server:

    def __init__(self, clients, port):

        self.clients = clients
        self.port = port
        self.socket = None
        self.running = False

    def start(self):

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 1024)
        print("Successfully created socket...")

        try:
            self.socket.bind(("", self.port))
            self.running = True
        except socket.error as err:
            print("Failed to bind socket: [{0}] {1}".format(err[0], err[1]))
            sys.exit()

        # Main server loop
        while self.running:

            sleep(1 / 1000)

            self.socket.listen(self.clients)
            connection, address = self.socket.accept()
            print("Connected to {0}:{1}".format(address[0], address[1]))
            user = User(connection, self)
            user.start()

