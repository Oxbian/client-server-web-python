# Laboratoire 1 (8INF876) - Question 4
---

Le but de cette question est de réalisé un client et un serveur web. Les fonctionnalités et les documentations (installation, utilisation) sont décrites ci-dessous.

## Client

Le client peut réaliser une requête vers n'importe quelle serveur web et récupérer le contenu de la page. Le contenu est sauvegardé dans un fichier en local, et affiché sur le navigateur interne de l'interface. En cas d'erreur lors de l'obtention du contenu d'une page, le code d'erreur est affiché avec une image de chat et le nom du code de status.

## Serveur

Le serveur web est capable d'envoyer le contenu d'une page web, et de répondre en cas d'erreur avec un nombre limité de codes d'erreur décrit dans la [RFC du protocol HTTP](https://www.rfc-editor.org/rfc/rfc2616.txt).

## Installation

Ce projet nécessite quelques dépendances, pour son bon fonctionnement il est donc nécessaire de les installer.  
  
Un environnement virtuel Python peut être réaliser pour ce projet:

```bash
python3 -m venv .venv
```

Puis, il suffit d'installer les dépendances dans cet environnement virtuel Python.

```bash
source .bin/python3/activate
```

```pip
pip install -r requirements.txt
```

## Utilisation

### Client

Pour utiliser le client, il faut lancer le programme Python appelé `main.py` se trouvant dans le répertoire `client/`.  
Un exemple avec l'environnement virtuel Python:

```bash
.venv/bin/python3 clients/main.py
```

L'interface permet de se connecter à un site web, voici les formats d'URL supporté:
- www.google.com
- http://www.google.com
- https://www.google.com

Tout ces formats d'URL supportent la précision du port, pour cela rajouter un `:port` à la fin de votre requête:
- www.google.com:80
- www.google.com:443
- http://www.google.com:80
- https://www.google.com:443

Il est aussi possible d'ajouter un chemin spécifique vers une ressource demandé:
- www.google.com/index.html
- http://www.google.com/index.html
- https://www.google.com/index.html
- www.google.com/index.html:80
- www.google.com/index.html:443
- http://www.google.com/index.html:80
- https://www.google.com/index.html:443


