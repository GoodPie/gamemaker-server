from enum import Enum


receive_codes = {
    "PING": 0,
    "HANDSHAKE": 1,
    "DISCONNECT": 2,
}

handshake_codes = {
    "UNKNOWN": 0,
    "WAITING_ACK": 1,
    "COMPLETED": 2
}

