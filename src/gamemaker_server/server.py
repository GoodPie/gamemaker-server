import socket
import sys
import threading
from time import sleep

from gamemaker_server.client import Client


class Server:
    def __init__(self, max_clients, port):
        self.max_clients = max_clients
        self.clients = []
        self.clients_lock = threading.Lock()
        self.verified_clients = {}
        self.port = port
        self.socket = None
        self.running = False

    def start(self):
        # Create a new socket
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Allow socket reuse to avoid "Address already in use" errors
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        try:
            # Attempt to bind socket to port
            self.socket.bind(("", self.port))
            self.running = True
        except socket.error as err:
            print("Failed to bind socket: {0}".format(err))
            sys.exit(1)

        # Listen for incoming connections (only needs to be called once)
        self.socket.listen(self.max_clients)
        print("Server listening on port {0}...".format(self.port))

        # Main server loop
        while self.running:
            sleep(1 / 1000)

            # Accept incoming connections
            connection, address = self.socket.accept()

            # Add user to user list and start the user thread
            print("Connected to {0}:{1}".format(address[0], address[1]))
            client = Client(connection, address, self)
            client.start()

            with self.clients_lock:
                self.clients.append(client)

    def remove_client(self, client):
        """Thread-safe removal of a client from the clients list."""
        with self.clients_lock:
            if client in self.clients:
                self.clients.remove(client)
