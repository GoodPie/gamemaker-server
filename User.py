import struct
import threading
import socket


class User(threading.Thread):
    def __init__(self, connection, server):
        # Initialize the thread
        threading.Thread.__init__(self)

        # Initialize class fields
        self.connection = connection
        self.server = server
        self.connected = True

    def run(self):
        while self.connected:
            # Receive data from clients
            data = self.connection.recv(1024)
            event_id = struct.unpack('B', data[:1])[0]

            # Determine what to do based on event id
            if event_id == 0:
                print(self.connection.send(data))

