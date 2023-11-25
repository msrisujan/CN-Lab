import socket
import threading
IP = socket.gethostbyname(socket.gethostname())
PORT = 5432
ADDR = (IP, PORT)
SIZE = 1024
DISCONNECT_MESSAGE = "!DISCONNECT"

def handle_client(conn, addr):
    connected = True
    while connected:
        msg = conn.recv(SIZE).decode()
        if msg == DISCONNECT_MESSAGE:
            connected = False
        
        if msg:
            print(f"{addr} {msg}")
    print("Disconnected!")
    conn.close()


def main():
    print("[STARTING] Server is starting...")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)
    server.listen()
    print(f"[LISTENING] Server is listening on {IP}:{PORT}")

    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()

if __name__=="__main__":
    main()