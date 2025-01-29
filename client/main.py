import os
import sys
from client_socket import httpClient
from PyQt5.QtCore import QSize, Qt, QUrl
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QLineEdit, QVBoxLayout, QWidget, QHBoxLayout
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineProfile

class MainWindow(QMainWindow):
    """Classe de gestion de la fenêtre"""

    def __init__(self):
        super().__init__()
        
        # Récupère le chemin absolu du fichier
        self.path = os.path.dirname(__file__)
 
        self.client = httpClient()
        self.setWindowTitle("Client web - Laboratoire 1")
        self.search_window()

    def connect(self):
        print("Connexion en cours...")

        self.connectBtn.setEnabled(False)

        # Connexion au socket à partir de l'IP fournie par l'utilisateur
        self.client.connect(self.connectInput.text())
        self.setWindowTitle("Connecter à: " + self.client.get_url())
        status = self.client.get_ressource()

        self.show_web(status, self.client.get_url())

    def search_window(self):
        """Affichage de l'interface de connexion à un site web"""

        # Création du contenu de l'interface par défaut
        label = QLabel("URL: ")
        self.connectInput = QLineEdit("www.google.com")
        self.connectBtn = QPushButton("Se connecter")
        self.connectBtn.clicked.connect(self.connect)

        self.setFixedSize(QSize(800, 500))

        hlayout = QHBoxLayout()
        hlayout.addWidget(label)
        hlayout.addWidget(self.connectInput)

        vlayout = QVBoxLayout()
        vlayout.addLayout(hlayout)
        vlayout.addWidget(self.connectBtn)

        container = QWidget()
        container.setLayout(vlayout)

        # Set the central widget of the Window.
        self.setCentralWidget(container)

    def show_web(self, status, url):
        """Affichage du contenu de la page ou de la page d'erreur"""

        print(f"Chemin: {self.path}")
        browser = QWebEngineView()
        if (status == "200"):
            browser.setUrl(QUrl.fromLocalFile(self.path + "/cache/" + url + ".html"))
        else:
            browser.setUrl(QUrl("https://http.cat/" + str(status)))

        searchBtn = QPushButton("Effectuer une nouvelle requête")
        searchBtn.clicked.connect(self.search_window)

        vlayout = QVBoxLayout()
        vlayout.addWidget(browser)
        vlayout.addWidget(searchBtn)

        container = QWidget()
        container.setLayout(vlayout)

        # Définit la taille de la fenêtre
        self.setCentralWidget(container)
        self.resize(1024, 768)
        return

def main():
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    app.exec()

if __name__ == "__main__":
    main()
