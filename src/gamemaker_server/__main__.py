import os

from gamemaker_server.server import Server


def main():
    port = int(os.environ.get("GAMEMAKER_PORT", 64198))
    max_clients = int(os.environ.get("GAMEMAKER_MAX_CLIENTS", 32))

    server = Server(max_clients, port)
    server.start()


if __name__ == "__main__":
    main()
