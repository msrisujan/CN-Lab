import socket
import threading
IP = socket.gethostbyname(socket.gethostname())
PORT = 6677
ADDR = (IP, PORT)
SIZE = 1024
DISCONNECT_MESSAGE = "!DISCONNECT"

clients = []

def check(conn, addr):
    while True:
        msg = conn.recv(SIZE).decode()
        k = 0
        if msg:
            for client in clients:
                if client["addr"] == addr:
                    conn.send("OK".encode())
                    k = 1
            if k != 1:
                if len(clients) != 5:
                    conn.send("OK".encode())
                    clients.append({"addr":addr, "conn":conn})
                else:
                    conn.send("NO".encode())


def main():
    print("[STARTING] Server is starting...")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)
    server.listen()
    print(f"[LISTENING] Server is listening on {IP}:{PORT}")

    while True:
        conn, addr = server.accept()
        # clients.append({"addr":addr, "conn":conn})
        thread = threading.Thread(target=check, args=(conn,addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")

if __name__=="__main__":
    main()