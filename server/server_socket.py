import socket

class httpServer:
    def __init__(self, _host = "0.0.0.0", _port = 8080, _max_connection = 3):
        self.host = _host
        self.port = _port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.max_connection = _max_connection # Nombre de connexion non accepté avant que le système refuse de nouvelles connexion (Anti DOS) 
            
    def listen_connexion(self):
        self.socket.bind((self.host, self.port))
        self.socket.listen(self.max_connection) # Définir la limite
        print("Serveur is listening...")

        while True:
            client_socket, client_addr = self.socket.accept()
            print(f"Connexion accepté de {client_addr}")

            self.handle_client(client_socket, client_addr)

    def handle_client(self, client_socket, client_addr):
        """Gestion du socket client, de sa demande et renvoi des données souhaitées"""
        request = client_socket.recv(4096).decode('utf-8')
        print(f"Requête reçue: {request}")


        response = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n<!doctype html><html><body><h1>Ok</h1></body></html>\r\n"
        client_socket.sendall(response.encode('utf-8'))
        client_socket.close()
