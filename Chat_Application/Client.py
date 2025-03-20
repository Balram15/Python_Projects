import socket
import threading

def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            print(message)
        except Exception as e:
            print(f"[ERROR] {e}")
            client_socket.close()
            break

def send_messages(client_socket):
    while True:
        message = input()
        try:
            client_socket.send(message.encode('utf-8'))
        except Exception as e:
            print(f"[ERROR] {e}")
            client_socket.close()
            break

def start_client():
    host = '127.0.0.1'
    port = 12345

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((host, port))
        print("Connected to the server!")
    except Exception as e:
        print(f"[ERROR] {e}")
        return

    threading.Thread(target=receive_messages, args=(client_socket,)).start()
    send_messages(client_socket)

if __name__ == "__main__":
    start_client()