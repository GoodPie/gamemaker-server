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

The server starts on port 64198 and accepts up to 32 clients.
