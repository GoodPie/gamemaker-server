# gamemaker-server

Multi-threaded TCP game server for GameMaker:Studio (or any game engine).

## Requirements

- Python 3.8+

## Running the Server

Install dependencies:

```bash
uv sync
```

Start the server:

```bash
python -m gamemaker_server
```

## Configuration

Configure the server using environment variables:

| Variable | Description | Default |
|----------|-------------|---------|
| `GAMEMAKER_PORT` | Server port | 64198 |
| `GAMEMAKER_MAX_CLIENTS` | Maximum client connections | 32 |

Example:

```bash
GAMEMAKER_PORT=8080 GAMEMAKER_MAX_CLIENTS=64 python -m gamemaker_server
```

## Protocol

This server uses a raw binary protocol. GameMaker clients must use the raw networking functions:

- `network_send_raw()` - Send data without GameMaker headers
- `network_send_udp_raw()` - Send UDP data without headers

Standard `network_send_packet()` adds GameMaker-specific headers that this server does not parse.

### Message Format

Messages use a simple 1-byte event ID prefix:

| Event ID | Name | Description |
|----------|------|-------------|
| 0 | PING | Echo request (server echoes back) |
| 1 | HANDSHAKE | Connection establishment |
| 2 | DISCONNECT | Clean disconnection |
