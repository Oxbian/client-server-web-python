import socket
import ssl
import sys
import re

class httpClient:
    def __init__(self):
        self.port = 80
        self.is_ssl = False

    def parse_url(self, url):
        """Récupération des données importantes dans l'URL"""
        self.url = url

        # Récupération du protocol
        if "http://" in self.url:
            self.url = url.split('http://', 1)[1]
        if "https://" in self.url:
            self.url = url.split('https://', 1)[1]
            self.port = 443
            self.is_ssl = True

        # Récupération du port
        if ':' in self.url:
            self.url, self.port = url.split(':', 1)
      
        # Récupération du chemin de la ressource
        if '/' in self.url:
            self.url, self.chemin = self.url.split('/', 1)
        else:
            self.chemin = '/'

    def is_ip(self, s):
        """Vérificateur de si la chaine de caractère est sous forme d'adresse IP"""
        ipv4_regex = r'^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'
        return bool(re.match(ipv4_regex, s))

    def get_ip(self):
        """Récupération de l'adresse IP pour le socket"""
        if self.is_ip(self.url):
            self.ip = self.url
        else:
            print(f"Récupération de l'IP pour {self.url}")
            self.ip = socket.gethostbyname(self.url)

        print(f"Connexion à: {self.ip}:{self.port}")

    def connect(self, url):
        """Connecte le socket à l'URL voulu par l'utilisateur"""
        
        try: 
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except socket.error as err:
            print(f"Erreur lors de la création du socket: {err}")

        self.parse_url(url)
        self.get_ip()
        
        if self.is_ssl:
            context = ssl.create_default_context()
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE
            self.socket = context.wrap_socket(self.socket, server_hostname=self.url)

        self.socket.connect((self.ip, int(self.port)))


    def get_ressource(self):
        """Utilise la méthode GET pour récupérer le contenu d'une page web"""
        if self.is_ssl:
            request = "GET " + self.chemin + " HTTP/1.1\r\nScheme: https\r\nHost: " + self.url + ":" + str(self.port) + "\r\nUser-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:134.0) Gecko/20100101 Firefox/134.0\r\nConnection: keep-alive\r\n\r\n" 
        else:
            request = "GET " + self.chemin + " HTTP/1.1\r\nHost: " + self.url + ":" + str(self.port) + "\r\nUser-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:134.0) Gecko/20100101 Firefox/134.0\r\n\r\n" 

        print(f"Sending: {request}")
        self.socket.send(request.encode())

        f = open(self.url + ".html", "w")

        data = self.socket.recv(4096).decode('utf-8', errors='replace')

        canWrite = False
        finished = False
        self.status = "200"

        while data and not finished and self.status == "200":
            print(data)
            for line in data.split("\n"):
                # Récupération du code de status de la réponse
                if "http/1.1" in line.lower():
                    self.status = line.split(' ')[1]
                    print(f"Status: {self.status}")

                # Recherche du début du contenu à écrire
                if "<!doctype html>" in line.lower():
                    canWrite = True

                # Recherche de la fin du contenu à écrire
                if "</html>" in line.lower():
                    finished = True

                if canWrite:
                    if finished:
                        index = line.find('</html>')
                        if index != -1:
                            f.write(line[:index + len('</html>')])
                    else:
                        f.write(line)

            if not finished and self.status == "200":
                data = self.socket.recv(4096).decode('utf-8', errors='replace')
        
        print("No more data")
        f.close()
        self.socket.close()
        return self.status

    def get_url(self) -> str:
        """Retourne l'URL utiliser pour la connexion"""
        return self.url
