import socket
import sys
import re

class httpClient:
    def is_ip(self, s):
        """Vérificateur de si la chaine de caractère est sous forme d'adresse IP"""
        ipv4_regex = r'^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'
        return bool(re.match(ipv4_regex, s))

    def connect(self, url):
        """Connecte le socket à l'URL voulu par l'utilisateur"""

        try: 
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except socket.error as err:
            print(f"Erreur lors de la création du socket: {err}")

        # Récupération du port
        if ':' in url:
            self.url, self.port = url.split(':', 1)
        else:
            self.port = 80
            self.url = url
      
        # Récupération du chemin de la ressource
        if '/' in self.url:
            self.url, self.chemin = self.url.split('/', 1)
        else:
            self.chemin = '/'

        # Récupération de l'adresse IP
        if self.is_ip(self.url):
            self.ip = self.url
        else:
            self.ip = socket.gethostbyname(self.url)

        print(f"Connexion à: {self.ip}:{self.port}")

        self.socket.connect((self.ip, self.port))


    def get_ressource(self):
        """Utilise la méthode GET pour récupérer le contenu d'une page web"""
        request = "GET " + self.chemin + " HTTP/1.1\r\nHost: " + self.url + ":" + str(self.port) + "\r\nUser-Agent: UQAC-Project\r\n\r\n" 
        print(f"Sending: {request}")
        self.socket.send(request.encode())

        f = open(self.url + ".html", "w")

        data = self.socket.recv(4096).decode('utf-8', errors='replace')

        canWrite = False
        finished = False
        self.status = "200"

        while data and not finished and self.status == "200":
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
