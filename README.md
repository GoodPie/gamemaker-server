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
