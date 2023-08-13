import socket
import threading
import sys

IP = socket.gethostbyname(socket.gethostname())
PORT = 5566
ADDR = (IP, PORT)
SIZE = 1024
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"

clients = []


def send_msg():
    while True:
        addr_input = input("Enter (ip port): ")
        addr_input = (addr_input.split()[0], int(addr_input.split()[1]))
        msg_input = input("Message: ")
        for client in clients:
            if client["addr"] == addr_input:
                try:
                    client["conn"].send(msg_input.encode(FORMAT))
                except BrokenPipeError:
                    print(f"[ERROR] Cannot send message to {addr_input}")
                break
        else:
            print(f"[ERROR] Cannot send message to {addr_input}")


def handle_client(conn, addr):
    print(f"\r[NEW CONNECTION] {addr} connected.")

    connected = True
    while connected:
        msg = conn.recv(SIZE).decode(FORMAT)
        if msg == DISCONNECT_MESSAGE:
            connected = False
            for client in clients:
                if client["addr"] == addr:
                    clients.remove(client)
                    break
            else:
                print(f"[ERROR] Cannot disconnect {addr}")
        
        if not msg:
            for client in clients:
                if client["addr"] == addr:
                    clients.remove(client)
                    break
            else:
                print(f"[ERROR] Cannot disconnect {addr}")
            print(f"\r[DISCONNECT CONNECTION] {addr} disconnected.")
            print("Enter (ip port): ", end="")
            sys.stdout.flush()
            break

        print(f"\r[{addr}] {msg}")
        print("Enter (ip port): ", end="")
        sys.stdout.flush()
        try:
            conn.send("Msg received".encode(FORMAT))
        except BrokenPipeError:
            print(f"[ERROR] Cannot send message to {addr}")
            break

    conn.close()

def main():
    print(f"[STARTING] Server is starting...")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    server.bind(ADDR)

    server.listen()
    print(f"[LISTENING] Server is listening on {IP}:{PORT}")

    print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")

    thread_send = threading.Thread(target=send_msg)
    thread_send.start()
    
    while True:
        conn, addr = server.accept()
        clients.append({"conn": conn, "addr": addr})

        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        
        
        print(f"\r[ACTIVE CONNECTIONS] {threading.active_count() - 2}")
        print("Enter (ip port): ", end="")
        sys.stdout.flush()

if __name__ == "__main__":
    main()