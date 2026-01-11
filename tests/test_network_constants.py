"""Tests for network protocol constants."""

from gamemaker_server.network_constants import RECEIVE_CODES, HANDSHAKE_CODES


def test_receive_codes_values():
    """Verify RECEIVE_CODES have expected values."""
    assert RECEIVE_CODES["PING"] == 0
    assert RECEIVE_CODES["HANDSHAKE"] == 1
    assert RECEIVE_CODES["DISCONNECT"] == 2


def test_handshake_codes_values():
    """Verify HANDSHAKE_CODES have expected values."""
    assert HANDSHAKE_CODES["UNKNOWN"] == 0
    assert HANDSHAKE_CODES["WAITING_ACK"] == 1
    assert HANDSHAKE_CODES["COMPLETED"] == 2


def test_receive_codes_no_duplicates():
    """Verify no duplicate values in RECEIVE_CODES."""
    values = list(RECEIVE_CODES.values())
    assert len(values) == len(set(values)), "Duplicate values found in RECEIVE_CODES"


def test_handshake_codes_no_duplicates():
    """Verify no duplicate values in HANDSHAKE_CODES."""
    values = list(HANDSHAKE_CODES.values())
    assert len(values) == len(set(values)), "Duplicate values found in HANDSHAKE_CODES"
