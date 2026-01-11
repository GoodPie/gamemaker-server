"""Tests for the Client class."""

import struct
from unittest.mock import Mock, patch

import pytest

from gamemaker_server.client import Client, SOCKET_TIMEOUT, MAX_HANDSHAKE_ATTEMPTS
from gamemaker_server.network_constants import RECEIVE_CODES, HANDSHAKE_CODES


@pytest.fixture
def mock_socket():
    """Create a mock socket for testing."""
    socket = Mock()
    socket.recv = Mock(return_value=b"\x00")  # Default: return PING
    socket.send = Mock()
    socket.settimeout = Mock()
    return socket


@pytest.fixture
def mock_server():
    """Create a mock server for testing."""
    server = Mock()
    server.remove_client = Mock()
    return server


class TestClientInitialization:
    """Tests for Client.__init__."""

    def test_client_sets_socket_timeout(self, mock_socket, mock_server):
        """Client should set socket timeout on initialization."""
        client = Client(mock_socket, ("127.0.0.1", 12345), mock_server)

        mock_socket.settimeout.assert_called_once_with(SOCKET_TIMEOUT)

    def test_client_initial_state(self, mock_socket, mock_server):
        """Client should initialize with correct default state."""
        client = Client(mock_socket, ("127.0.0.1", 12345), mock_server)

        assert client.connected is True
        assert client.handshake == HANDSHAKE_CODES["UNKNOWN"]
        assert client.user is None
        assert client.address == ("127.0.0.1", 12345)


class TestClientProtocol:
    """Tests for Client message handling."""

    def test_ping_is_echoed_back(self, mock_socket, mock_server):
        """PING messages should be echoed back."""
        ping_data = struct.pack("B", RECEIVE_CODES["PING"])
        mock_socket.recv.side_effect = [ping_data, b""]  # PING then disconnect

        client = Client(mock_socket, ("127.0.0.1", 12345), mock_server)
        client.handshake = HANDSHAKE_CODES["COMPLETED"]  # Skip handshake
        client.run()

        # Verify ping was echoed
        mock_socket.send.assert_called_with(ping_data)

    def test_empty_data_disconnects(self, mock_socket, mock_server):
        """Empty recv data should trigger disconnect."""
        mock_socket.recv.return_value = b""

        client = Client(mock_socket, ("127.0.0.1", 12345), mock_server)
        client.handshake = HANDSHAKE_CODES["COMPLETED"]
        client.run()

        assert client.connected is False
        mock_server.remove_client.assert_called_once_with(client)

    def test_disconnect_message_disconnects(self, mock_socket, mock_server):
        """DISCONNECT message should trigger disconnect."""
        disconnect_data = struct.pack("B", RECEIVE_CODES["DISCONNECT"])
        mock_socket.recv.return_value = disconnect_data

        client = Client(mock_socket, ("127.0.0.1", 12345), mock_server)
        client.handshake = HANDSHAKE_CODES["COMPLETED"]
        client.run()

        assert client.connected is False


class TestClientHandshake:
    """Tests for Client.wait_for_handshake."""

    def test_successful_handshake(self, mock_socket, mock_server):
        """Handshake should complete when client responds correctly."""
        handshake_response = struct.pack("B", RECEIVE_CODES["HANDSHAKE"])
        mock_socket.recv.return_value = handshake_response

        client = Client(mock_socket, ("127.0.0.1", 12345), mock_server)
        result = client.wait_for_handshake()

        assert result is True
        assert client.handshake == HANDSHAKE_CODES["COMPLETED"]

    def test_handshake_sends_initial_message(self, mock_socket, mock_server):
        """Handshake should send HANDSHAKE message to client."""
        handshake_response = struct.pack("B", RECEIVE_CODES["HANDSHAKE"])
        mock_socket.recv.return_value = handshake_response

        client = Client(mock_socket, ("127.0.0.1", 12345), mock_server)
        client.wait_for_handshake()

        expected_message = struct.pack("B", RECEIVE_CODES["HANDSHAKE"])
        mock_socket.send.assert_called_with(expected_message)

    def test_handshake_fails_on_empty_data(self, mock_socket, mock_server):
        """Handshake should fail if client sends empty data."""
        mock_socket.recv.return_value = b""

        client = Client(mock_socket, ("127.0.0.1", 12345), mock_server)
        # Set state to WAITING_ACK to trigger recv
        client.handshake = HANDSHAKE_CODES["WAITING_ACK"]
        result = client.wait_for_handshake()

        assert result is False


class TestClientDisconnect:
    """Tests for Client.disconnect_user."""

    def test_disconnect_calls_server_remove(self, mock_socket, mock_server):
        """Disconnect should call server.remove_client."""
        client = Client(mock_socket, ("127.0.0.1", 12345), mock_server)
        client.disconnect_user()

        mock_server.remove_client.assert_called_once_with(client)
        assert client.connected is False

    def test_disconnect_only_runs_once(self, mock_socket, mock_server):
        """Multiple disconnect calls should only remove client once."""
        client = Client(mock_socket, ("127.0.0.1", 12345), mock_server)
        client.disconnect_user()
        client.disconnect_user()

        # Should only be called once
        assert mock_server.remove_client.call_count == 1
