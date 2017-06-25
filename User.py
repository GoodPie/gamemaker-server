import struct
import threading
import socket


class User(threading.Thread):
    def __init__(self, connection, address, server):
        # Initialize the thread
        threading.Thread.__init__(self)

        # Initialize class fields
        self.connection = connection
        self.address = address
        self.server = server
        self.connected = True

    def run(self):
        while self.connected:

            try:
                # Receive data from clients
                data = self.connection.recv(1024)

                # Determine what to do based on event id
                event_id = struct.unpack('B', data[:1])[0]
                if event_id == 0:
                    self.connection.send(data)
            except ConnectionResetError:
                self.disconnect_user()
            except struct.error:
                # This only appears when the user attempts to disconnect during loop
                # Will probably be removed when more data is handled so we can properly handle this error
                self.disconnect_user()

    def disconnect_user(self):
        print("Disconnected from {0}:{1}".format(self.address[0], self.address[1]))
        self.server.users.remove(self)
        self.connected = False
