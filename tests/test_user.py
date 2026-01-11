"""Tests for the User model."""

from gamemaker_server.user import User


def test_user_initialization():
    """Test User is initialized with correct values."""
    user = User(x=100, y=200, username="player1")

    assert user.x == 100
    assert user.y == 200
    assert user.username == "player1"


def test_user_attributes_can_be_modified():
    """Test User attributes can be changed after creation."""
    user = User(x=0, y=0, username="")

    user.x = 50
    user.y = 75
    user.username = "new_player"

    assert user.x == 50
    assert user.y == 75
    assert user.username == "new_player"
