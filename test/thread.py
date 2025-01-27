import socket
import threading

def client_request(i):
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(('127.0.0.1', 8080))

        request = "GET / HTTP/1.1\r\nHost: 127.0.0.1\r\n\r\n"
        client_socket.sendall(request.encode('utf-8'))

        response = client_socket.recv(1024)
        print(f"Réponse reçue de la connexion {i}:")
        print(response.decode('utf-8'))

        client_socket.close()
    except Exception as e:
        print(f"Erreur lors de la connexion {i}: {e}")

# Créer et démarrer plusieurs threads pour simuler des clients simultanés
threads = []
for i in range(5):  # Essayer avec 5 connexions simultanées
    thread = threading.Thread(target=client_request, args=(i,))
    threads.append(thread)
    thread.start()

for thread in threads:
    thread.join()
