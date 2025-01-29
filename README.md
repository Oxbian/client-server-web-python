# Laboratoire 1 (8INF876) - Question 4
---

Le but de cette question est de réalisé un client et un serveur web.  
Les fonctionnalités et les documentations (installation, utilisation) sont décrites ci-dessous.  

## Client

Le client peut réaliser une requête vers n'importe quelle serveur web et récupérer le contenu de la page.  
  
Le contenu est sauvegardé dans un fichier en local, et affiché sur le navigateur interne de l'interface. En cas d'erreur lors de l'obtention du contenu d'une page, le code d'erreur est affiché avec une image de chat et le nom du code de status.

## Serveur

Le serveur web est capable d'envoyer le contenu d'une page web, et de répondre en cas d'erreur avec un nombre limité de codes d'erreur décrit dans la [RFC du protocol HTTP](https://www.rfc-editor.org/rfc/rfc2616.txt).  
  
Les codes implémentés sont:  
- 200 OK, retourne le contenu de la ressource demandé  
- 400 Bad Request, la requête est mal formatée  
- 403 Forbidden, la ressource est interdite d'accès  
- 404 Not Found, la ressource demandée n'a pas été trouvée  
- 405 Method Not Allowed, la requête utilise une méthode autre que GET  
- 500 Internal Server Error, erreur lors de la lecture du fichier html défini en tant que ressource dans la configuration  
  
Un fichier de configuration est présent, et permet de définir des règles d'accès pour des ressources (autorisé, bloqué, ressources par défaut pour une URL...)  

Le fichier de configuration possède 2 grandes règles:  
- `config:`, qui permet de définir les règles de configuration du serveur comme l'IP d'écoute, le port, le nombre de tentative max de connexion sans acceptation du client sur le socket.  
- `routes: {chemin}`, qui permet de définir des routes pour le serveur, par défaut la route est autorisé (`allow`) et le fichier `index.html` sera retourné. Des routes peuvent être interdites avec le mot clé `disallow`. La ressource retournée par la route peut être définie grâce au mot clé `ressource:`  
  
Pour avoir un exemple de configuration vous pouvez aller voir le fichier `server/server.conf`.

Le serveur offre une route par défaut appelé `/info` qui affiche la requête réalisée par le client lors de la demande d'accès à une ressource.

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

### Serveur

Pour utiliser le serveur, il faut lancer le programme Python appelé `main.py` se trouvant dans le répertoire `server/`.  
  
**Attention, une configuration est attendue dans le fichier `server/server.conf`. Celle fournie par défaut est fonctionnelle, mais vous pouvez la modifier selon vos besoins**  
  
Un exemple avec l'environnement virtuel Python:  

```bash
.venv/bin/python3 server/main.py
```
