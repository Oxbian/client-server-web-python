# Client & serveur web
---

Ce projet est un client et serveur web réalisé en Python, utilisant uniquement les sockets de Python et pas de librairie permettant de simplifier le développement d'un client ou serveur web.

Les fonctionnalités et les documentations (installation, utilisation) sont décrites ci-dessous.  

## Fonctionnalités

### Client

Le client peut réaliser une requête vers n'importe quel serveur web et récupérer le contenu de la page.  
  
Le contenu est sauvegardé dans un fichier en local dans le répertoire `client/cache/`, et affiché sur le navigateur interne de l'interface. En cas d'erreur lors de l'obtention du contenu d'une page, le code d'erreur est affiché avec une image de chat et le nom du code de status.

### Serveur

Le serveur web est capable d'envoyer le contenu d'une page web et de répondre en cas d'erreur avec un nombre limité de codes d'erreur décrits dans la [RFC du protocole HTTP](https://www.rfc-editor.org/rfc/rfc2616.txt).  
  
Les codes implémentés sont :  
- 200 OK, retourne le contenu de la ressource demandé  
- 400 Bad Request, la requête est mal formatée  
- 403 Forbidden, la ressource est interdite d'accès  
- 404 Not Found, la ressource demandée n'a pas été trouvée  
- 405 Method Not Allowed, la requête utilise une méthode autre que GET  
- 500 Internal Server Error, erreur lors de la lecture du fichier HTML défini en tant que ressource dans la configuration  
  
Un fichier de configuration est présent et permet de définir des règles d'accès pour des ressources (autorisé, bloqué, ressources par défaut pour une URL...)  

Le fichier de configuration possède 2 grandes règles :  
- `config:`, qui permet de définir les règles de configuration du serveur comme l'IP d'écoute, le port, le nombre de tentatives maximum de connexion sans acceptation du client sur le socket.  
- `routes: {chemin}`, qui permet de définir des routes pour le serveur, par défaut, la route est autorisée (`allow`) et le fichier `index.html` sera retourné. Des routes peuvent être interdites avec le mot-clé `disallow`. La ressource retournée par la route peut être définie grâce au mot-clé `ressource:`  
  
Pour avoir un exemple de configuration, vous pouvez aller voir le fichier `server/server.conf`.

Le serveur offre une route par défaut appelée `/info` qui affiche la requête réalisée par le client lors de la demande d'accès à une ressource.

## Démarrage

Suivez les étapes ci-dessous pour configurer et exécuter le projet localement.

### Prérequis

Ces programmes sont nécessaires pour le bon fonctionnement du projet :

- Python3.8

### Installation

Ce projet nécessite quelques dépendances, pour son bon fonctionnement il est donc nécessaire de les installer.  
  
Un environnement virtuel Python peut être réalisé pour ce projet :

```bash
python3 -m venv .venv
```

Puis, il faut installer les dépendances dans cet environnement virtuel Python.

```bash
source .bin/python3/activate
```

```pip
pip install -r requirements.txt
```

### Utilisation

#### Client

Pour utiliser le client, il faut lancer le programme Python appelé `main.py` se trouvant dans le répertoire `client/`.  
Un exemple avec l'environnement virtuel Python :

```bash
.venv/bin/python3 clients/main.py
```

L'interface permet de se connecter à un site web, voici les formats d'URL supporté :
- www.google.com
- http://www.google.com
- https://www.google.com

Tout ces formats d'URL supportent la précision du port, pour cela rajouter un `:port` à la fin de votre requête :
- www.google.com:80
- www.google.com:443
- http://www.google.com:80
- https://www.google.com:443

Il est aussi possible d'ajouter un chemin spécifique vers une ressource demandée :
- www.google.com/index.html
- http://www.google.com/index.html
- https://www.google.com/index.html
- www.google.com/index.html:80
- www.google.com/index.html:443
- http://www.google.com/index.html:80
- https://www.google.com/index.html:443

#### Serveur

Pour utiliser le serveur, il faut lancer le programme Python appelé `main.py` se trouvant dans le répertoire `server/`.  
  
**Attention, une configuration est attendue dans le fichier `server/server.conf`. Celle fournie par défaut est fonctionnelle, mais vous pouvez la modifier selon vos besoins**  
  
Un exemple avec l'environnement virtuel Python :  

```bash
.venv/bin/python3 server/main.py
```

## Fonctionnement

### Client

1. **Saisie de l'URL et recherche :** L'utilisateur saisit une URL valide (les formats supportés sont décrits plus haut), puis clique sur le bouton "Se connecter".
2. **Connexion au serveur web :** Le client recherche l'adresse IP derrière l'URL saisie par l'utilisateur et crée un socket sur cette adresse IP + port (fournie ou non par l'utilisateur). Une fois ce socket créé, le client envoie une requête *HTTP GET* pour récupérer le contenu demandé par l'utilisateur.

Si le client demande de réaliser une requête avec le protocole HTTPS, alors la requête envoyée sera de la forme :
```
GET {chemin} HTTP/1.1\r
Scheme: https\r
Host: {url}:{port}\r
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:134.0) Gecko/20100101 Firefox/134.0\r
Connection: keep-alive\r
\r
```
*L'utilisation d'un `User-Agent` venant d'un navigateur web sous Firefox permet de contourner les restrictions de certains serveurs web (Amazon, Netflix, ...).*

Si le client demande de réaliser une requête avec le protocole HTTP, alors la requête envoyée sera de la forme :
```
GET {chemin} HTTP/1.1\r
Host: {url}:{port}\r\
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:134.0) Gecko/20100101 Firefox/134.0\r
\r
```

3. **Récupération de la réponse & sauvegarde :** La réponse du serveur web est sauvegardée dans un fichier du format `url.html` dans le répertoire `client/cache/`, si le serveur a répondu avec le code 200. 
4. **Affichage de la page web :** Si une page à été sauvegardée (status 200), alors elle est affiché sur le navigateur interne de l'interface Qt. Sinon une image de chat venant du site [http.cat](https://http.cat) sera retournée avec le code de status répondu par le serveur web.

### Serveur

1. **Récupération de la configuration :** La configuration du serveur web se trouvant dans `serveur/server.conf` est lue, et permet de configurer le serveur (IP d'écoute, port d'écoute, nombre de connexions sans réponse maximale pour un socket, routes et ressources à fournir).
2. **Création d'un socket d'écoute :** Le serveur web crée un socket à l'écoute d'une connexion d'un client, puis va traiter la requête du client.
3. **Traitement de la requête :** La ressource demandée par le client est comparée avec la configuration du serveur et la réponse sera créée en fonction. Une ressource non autorisée dans la configuration répondra avec un code de status *403*, tandis qu'une ressource autorisée répondra avec un *200* et le contenu d'une page HTML à afficher sur le client.
4. **Fermeture de la connexion :** La connexion du client sur le socket du serveur est fermée, puisque la requête a été traitée par le serveur.
