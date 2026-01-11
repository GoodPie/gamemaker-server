import socket
import struct
import threading

from gamemaker_server.network_constants import RECEIVE_CODES, HANDSHAKE_CODES

# Timeout for socket operations in seconds
SOCKET_TIMEOUT = 30.0
# Maximum handshake attempts before giving up
MAX_HANDSHAKE_ATTEMPTS = 10


class Client(threading.Thread):
    def __init__(self, connection, address, server):
        threading.Thread.__init__(self)

        # Connection Information
        self.connection = connection
        # Set socket timeout to prevent hanging on dead connections
        self.connection.settimeout(SOCKET_TIMEOUT)
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
        if not self.wait_for_handshake():
            self.disconnect_user()
            return

        # Handshake complete so execute main data read loop
        while self.connected:
            try:
                # Receive data from clients
                data = self.connection.recv(1024)

                # Empty data means client disconnected gracefully
                if not data:
                    self.disconnect_user()
                    break

                # Parse event ID from first byte
                try:
                    event_id = struct.unpack("B", data[:1])[0]
                except struct.error:
                    # Malformed data, disconnect client
                    self.disconnect_user()
                    break

                if event_id == RECEIVE_CODES["PING"]:
                    self.connection.send(data)
                elif event_id == RECEIVE_CODES["DISCONNECT"]:
                    self.disconnect_user()

            except socket.timeout:
                # Client timed out, disconnect
                print("Client {0} timed out".format(self.address[0]))
                self.disconnect_user()
            except ConnectionResetError:
                self.disconnect_user()
            except OSError:
                # Broken pipe or other socket error
                self.disconnect_user()

    def wait_for_handshake(self):
        """Wait for the handshake to complete before reading any other info.

        Returns True if handshake succeeded, False otherwise.
        """
        attempts = 0

        while self.connected and self.handshake != HANDSHAKE_CODES["COMPLETED"]:
            attempts += 1
            if attempts > MAX_HANDSHAKE_ATTEMPTS:
                print(
                    "Handshake with {0} failed: too many attempts".format(
                        self.address[0]
                    )
                )
                return False

            try:
                if self.handshake == HANDSHAKE_CODES["UNKNOWN"]:
                    # Send message to client letting them know we are handshaking
                    handshake = struct.pack("B", RECEIVE_CODES["HANDSHAKE"])
                    self.connection.send(handshake)
                    self.handshake = HANDSHAKE_CODES["WAITING_ACK"]

                else:
                    # Wait for handshake ack
                    data = self.connection.recv(1024)

                    # Empty data means client disconnected
                    if not data:
                        return False

                    try:
                        event_id = struct.unpack("B", data[:1])[0]
                    except struct.error:
                        return False

                    if event_id == RECEIVE_CODES["HANDSHAKE"]:
                        # Received handshake successfully from client
                        self.handshake = HANDSHAKE_CODES["COMPLETED"]
                        print("Handshake with {0} complete...".format(self.address[0]))

            except socket.timeout:
                print("Handshake with {0} timed out".format(self.address[0]))
                return False
            except (ConnectionResetError, OSError):
                return False

        return True

    def disconnect_user(self):
        """Remove the user from the server after disconnection."""
        if not self.connected:
            return

        print("Disconnected from {0}:{1}".format(self.address[0], self.address[1]))
        self.server.remove_client(self)
        self.connected = False
