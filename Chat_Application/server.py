import socket
import threading

# Server configuration
HOST = '127.0.0.1'  # Localhost
PORT = 12345       # Port to listen on

# List to keep track of clients
clients = []

def handle_client(client_socket, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break
            print(f"{addr} says: {message}")
            broadcast(message, client_socket)
        except Exception as e:
            print(f"[ERROR] {e}")
            break
    print(f"[DISCONNECTED] {addr} disconnected.")
    clients.remove(client_socket)
    client_socket.close()

def broadcast(message, sender_socket):
    for client in clients:
        if client != sender_socket:
            try:
                client.send(message.encode('utf-8'))
            except Exception as e:
                print(f"[ERROR] {e}")

# Main function to start the server
def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(5)
    print(f"[LISTENING] Server is listening on {HOST}:{PORT}")

    while True:
        client_socket, addr = server.accept()
        clients.append(client_socket)
        client_thread = threading.Thread(target=handle_client, args=(client_socket, addr))
        client_thread.start()

if __name__ == "__main__":
    start_server()
