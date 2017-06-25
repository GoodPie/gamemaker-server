import struct
import threading
import socket

from NetworkConstants import receive_codes, handshake_codes


class Client(threading.Thread):
    def __init__(self, connection, address, server):
        threading.Thread.__init__(self)

        self.connection = connection                        # Connection Information
        self.address = address                              # Client Address Properties
        self.server = server                                # Reference to main server
        self.connected = True                               # Connection status
        self.handshake = handshake_codes['UNKNOWN']         # Handshake status defaulted to unknown
        self.user = None                                    # Clients each have a user for the game

    def run(self):

        # Wait for handshake to complete before reading any data
        self.wait_for_handshake()

        # Handshake complete so execute main data read loop
        while self.connected:
            try:
                # Receive data from clients
                data = self.connection.recv(1024)
                event_id = struct.unpack('B', data[:1])[0]

                if event_id == receive_codes['PING']:
                    self.connection.send(data)
                elif event_id == receive_codes['DISCONNECT']:
                    self.disconnect_user()

            except ConnectionResetError:
                self.disconnect_user()

    def wait_for_handshake(self):
        """
            Wait for the handshake to complete before reading any other information
            TODO: Add better implementation for handshake
        """

        while self.connected and self.handshake != handshake_codes["COMPLETED"]:

            if self.handshake == handshake_codes['UNKNOWN']:
                # First send message to client letting them know we are engaging in a handshake
                handshake = struct.pack('B', receive_codes['HANDSHAKE'])
                self.connection.send(handshake)
                self.handshake = handshake_codes['WAITING_ACK']

            else:
                # Wait for handshake ack
                data = self.connection.recv(1024)
                event_id = struct.unpack('B', data[:1])[0]

                if event_id == receive_codes['HANDSHAKE']:
                    # Received handshake successfully from client
                    self.handshake = handshake_codes['COMPLETED']
                    print("Handshake with {0} complete...".format(self.address[0]))

    def disconnect_user(self):
        """
            Removes the user from the server after disconnection
            TODO: Pass actual server as reference so we can modify it
        """
        print("Disconnected from {0}:{1}".format(self.address[0], self.address[1]))
        self.server.users.remove(self)
        self.connected = False
