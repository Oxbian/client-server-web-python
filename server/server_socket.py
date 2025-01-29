import socket
from datetime import datetime
from pathlib import Path

class httpServer:
    def __init__(self, _config, _curr_dir):
        self.host = _config.get_host() or "0.0.0.0"
        self.port = _config.get_port() or 8080
        # Nombre de connexion non accepté avant que le système refuse de nouvelles connexion (Anti DOS) 
        self.max_connection = _config.get_max_conn() or 3

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.config = _config
        self.path = _curr_dir 

    def listen_connexion(self):
        """Lancement de l'écoute du serveur et ouverture d'une session avec le client"""

        self.socket.bind((self.host, self.port))
        self.socket.listen(self.max_connection)
        print("Serveur is listening...")

        while True:
            client_socket, client_addr = self.socket.accept()
            print(f"Connexion accepté de {client_addr}")

            self.handle_client(client_socket, client_addr)

    def handle_client(self, client_socket, client_addr):
        """Gestion du socket client, de sa demande et renvoi des données souhaitées"""
        request = client_socket.recv(4096).decode('utf-8')

        response = self.handle_request(request)

        client_socket.sendall(response.encode('utf-8'))
        client_socket.close()

    def handle_request(self, request):
        """Gestion de la requête, retourne la page ou le code d'erreur correspondant à la requête"""

        status = 400
        content = ""

        # Parser la requête
        try:
            method, ressource, protocol = request.split('\n')[0].split(" ")
            print(f"Requête reçue: {method} {ressource} {protocol}")
        except ValueError:
            print(f"Requête mal formattée: {request}")
            status = 400
        
        # Si GET, alors récupérer le chemin, sinon méthode non authorisé
        if method.lower() == "get":
            if ressource == "info":
                status = 200
                page = "info.html"
            else:
                status, page = self.config.get_route(ressource)
        # Lecture du contenu de la page
            try:
                with open(self.path / "pages" / page, "r") as file:
                    content = file.read()
                    print(content)
            except Exception as e:
                print(f"Une erreur inattendue est survenue : {e}")
                status = 500
        else:
            status = 405

        # Créer la réponse
        date_utc = datetime.utcnow()
        date_str = date_utc.strftime("%a, %d %b %Y %H:%M:%S GMT")

        if status == 200:
            content_length = len(content)
            response = f"{protocol} 200 OK\r\nDate: {date_str}\r\nContent-Type: text/html; charset=UTF-8\r\nContent-Length: {content_length}\r\n\r\n{content}"
        elif status == 400:
            response = f"{protocol} 400 Bad Request\r\nDate: {date_str}\r\nContent-Type: text/html; charset=UTF-8"
        elif status == 403:
            response = f"{protocol} 403 Forbidden\r\nDate: {date_str}\r\nContent-Type: text/html; charset=UTF-8"
        elif status == 404:
            response = f"{protocol} 404 Not Found\r\nDate: {date_str}\r\nContent-Type: text/html; charset=UTF-8"
        elif status == 405:
            response = f"{protocol} 405 Method Not Allowed\r\nDate: {date_str}\r\nContent-Type: text/html; charset=UTF-8\r\nAllow: GET"
        elif status == 500:
            response = f"{protocol} 500 Internal Server Error\r\nDate: {date_str}\r\nContent-Type: text/html; charset=UTF-8"

        return response
