import socket
from server_socket import httpServer

def main():
    # Lire la config
    # Autoriser les fichiers et bannir certains autres
    # Multithreading pour gestion de plusieurs clients

    # Les valeurs par défaut du serveur seront récupérées depuis la config
    server = httpServer()
    server.listen_connexion()


if __name__ == "__main__":
    main()


