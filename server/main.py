import socket
from pathlib import Path
from server_socket import httpServer
from server_config import Config

def main():
    # Les valeurs par défaut du serveur seront récupérées depuis la config
    curr_dir = Path(__file__).parent
    conf_filepath = curr_dir / "server.conf"

    config = Config(conf_filepath)
    config.parse_config()

    server = httpServer(config, curr_dir)
    server.listen_connexion()


if __name__ == "__main__":
    main()


