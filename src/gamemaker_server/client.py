import struct
import threading

from gamemaker_server.network_constants import RECEIVE_CODES, HANDSHAKE_CODES


class Client(threading.Thread):
    def __init__(self, connection, address, server):
        threading.Thread.__init__(self)

        # Connection Information
        self.connection = connection
        # Client Address Properties
        self.address = address
        # Reference to main server
        self.server = server
        # Connection status
        self.connected = True
        # Handshake status defaulted to unknown
        self.handshake = HANDSHAKE_CODES["UNKNOWN"]
        # Clients each have a user for the game
        self.user = None

    def run(self):
        # Wait for handshake to complete before reading any data
        self.wait_for_handshake()

        # Handshake complete so execute main data read loop
        while self.connected:
            try:
                # Receive data from clients
                data = self.connection.recv(1024)
                event_id = struct.unpack("B", data[:1])[0]

                if event_id == RECEIVE_CODES["PING"]:
                    self.connection.send(data)
                elif event_id == RECEIVE_CODES["DISCONNECT"]:
                    self.disconnect_user()

            except ConnectionResetError:
                self.disconnect_user()

    def wait_for_handshake(self):
        """Wait for the handshake to complete before reading any other info.

        TODO: Add better implementation for handshake
        """
        while self.connected and self.handshake != HANDSHAKE_CODES["COMPLETED"]:

            if self.handshake == HANDSHAKE_CODES["UNKNOWN"]:
                # Send message to client letting them know we are handshaking
                handshake = struct.pack("B", RECEIVE_CODES["HANDSHAKE"])
                self.connection.send(handshake)
                self.handshake = HANDSHAKE_CODES["WAITING_ACK"]

            else:
                # Wait for handshake ack
                data = self.connection.recv(1024)
                event_id = struct.unpack("B", data[:1])[0]

                if event_id == RECEIVE_CODES["HANDSHAKE"]:
                    # Received handshake successfully from client
                    self.handshake = HANDSHAKE_CODES["COMPLETED"]
                    print("Handshake with {0} complete...".format(self.address[0]))

    def disconnect_user(self):
        """Remove the user from the server after disconnection.

        TODO: Pass actual server as reference so we can modify it
        """
        print("Disconnected from {0}:{1}".format(self.address[0], self.address[1]))
        self.server.clients.remove(self)
        self.connected = False
