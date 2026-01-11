"""Tests for the Server class."""

import threading
from unittest.mock import Mock

import pytest

from gamemaker_server.server import Server


class TestServerInitialization:
    """Tests for Server.__init__."""

    def test_server_initialization(self):
        """Server should initialize with correct values."""
        server = Server(max_clients=32, port=64198)

        assert server.max_clients == 32
        assert server.port == 64198
        assert server.clients == []
        assert server.running is False
        assert server.socket is None

    def test_server_has_clients_lock(self):
        """Server should have a threading lock for clients."""
        server = Server(max_clients=32, port=64198)

        assert hasattr(server, "clients_lock")
        assert isinstance(server.clients_lock, type(threading.Lock()))


class TestServerRemoveClient:
    """Tests for Server.remove_client."""

    def test_remove_client_removes_from_list(self):
        """remove_client should remove client from clients list."""
        server = Server(max_clients=32, port=64198)
        mock_client = Mock()
        server.clients.append(mock_client)

        server.remove_client(mock_client)

        assert mock_client not in server.clients

    def test_remove_client_handles_missing_client(self):
        """remove_client should not error if client not in list."""
        server = Server(max_clients=32, port=64198)
        mock_client = Mock()

        # Should not raise
        server.remove_client(mock_client)

    def test_remove_client_is_thread_safe(self):
        """remove_client should be thread-safe."""
        server = Server(max_clients=32, port=64198)

        # Add multiple clients
        clients = [Mock() for _ in range(10)]
        for client in clients:
            server.clients.append(client)

        # Remove clients from multiple threads
        threads = []
        for client in clients:
            t = threading.Thread(target=server.remove_client, args=(client,))
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

        assert len(server.clients) == 0
