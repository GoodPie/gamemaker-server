from gamemaker_server.server import Server

if __name__ == "__main__":
    server = Server(32, 64198)
    server.start()
