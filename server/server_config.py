
class Config:
    def __init__(self, config_filepath):
        self.file = open(config_filepath, "r")
        self.host = None
        self.port = None
        self.max_conn = None
        self.routes = {}


    def parse_config(self):
        """Parsing du fichier de config à la recherche des paramètres et règles de routes"""

        current_section = None

        for line in self.file.readlines():
            line = line.lower().strip()
            
            if line == "":
                continue

            if line.startswith("config:"):
                current_section = "config"
            elif line.startswith("routes:"):
                current_section = "routes"
                self.parse_route_line(line)

            elif current_section == "routes":
                self.parse_route_line(line)
            elif current_section == "config":
                self.parse_config_line(line)


    def parse_config_line(self, line):
        """Parser la section config"""

        if line.startswith("host:"):
            self.host = line.split(":")[1].strip()
        elif line.startswith("port:"):
            self.port = int(line.split(":")[1].strip())
        elif line.startswith("max_connection:"):
            self.max_conn = int(line.split(":")[1].strip())


    def parse_route_line(self, line):
        """Parser une section route"""

        if line.startswith("routes:"):
            self.parse_route = line.split(":", 1)[1].strip()
            self.routes[self.parse_route] = "index.html"

        if line.startswith("disallow"):
            self.routes[self.parse_route] = 403
        
        if line.startswith("ressource:"):
            self.routes[self.parse_route] = line.split(":", 1)[1].strip()


    def get_host(self):
        """Getter pour retourner l'IP d'écoute du serveur"""
        return self.host


    def get_port(self):
        """Getter pour retourner le port d'écoute du serveur"""
        return self.port


    def get_max_conn(self):
        """Getter pour retourner le nombre maximale de connexion avant de refuser"""
        return self.max_conn


    def get_route(self, route):
        """Retourne le code de status, et la page par défaut de la route demandée"""
        status, page = 404, None

        if route in self.routes.keys():
            page = self.routes[route]

            if page == 403:
                status = 403
                page = None
            else:
                status = 200

        return status, page


    def __del__(self):
        self.file.close()
