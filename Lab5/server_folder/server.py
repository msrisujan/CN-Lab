import socket
import threading
import readline
import time

IP = socket.gethostbyname(socket.gethostname())
PORT = 5567
ADDR = (IP, PORT)
SIZE = 1024
FORMAT = "utf-8"
DISCONNECT_MSG = "!DISCONNECT"

clients = []

current_input = ""

def print_msg(msg):
    input_buffer = readline.get_line_buffer()
    print(f"\r{msg}\n{current_input}{input_buffer}",end="",flush=True)

def input_msg(input_str):
    global current_input
    current_input = input_str
    output = input(f"\r{input_str}")
    return output

def handle_client(conn,addr):
    print_msg(f"[NEW CONNECTION] {addr} connected.")

    connected = True
    while connected:

        file_name = conn.recv(SIZE).decode(FORMAT)
        if file_name == DISCONNECT_MSG:
            connected = False
            print_msg(f"[DISCONNECTED] {addr} disconnected.")
            for client in clients:
                if client["addr"] == addr:
                    clients.remove(client)
                    break
            else:
                print_msg(f"[ERROR] Cannot disconnect {addr}")
        else:
            msg_type = file_name.split(":")[0]
            msg = file_name.split(":")[1]
            if msg_type == "f":
                print_msg(f"{addr}, file: {msg}")
                file = open(msg,"w")
                conn.send("w:File created".encode(FORMAT))
                data = conn.recv(SIZE).decode(FORMAT)
                time.sleep(0.1)
                file.write(data)
                conn.send("w:Data received and saved in file".encode(FORMAT))
                file.close()
            elif msg_type == "w":
                print_msg(f"{addr}, msg: {msg}")
            else:
                print_msg(f"[ERROR] Unknown message type: {msg_type}")

    conn.close()

def send_file():
    while True:
        addr_input = input_msg("Enter (ip port): ")
        addr_input = (addr_input.split()[0], int(addr_input.split()[1]))
        file_name = input_msg("Enter the file name: ")
        if file_name == DISCONNECT_MSG:
            for client in clients:
                if client["addr"] == addr_input:
                    client["conn"].send(file_name.encode(FORMAT))
                    clients.remove(client)
                    break
        file = open(file_name,"r")
        data = file.read()
        file.close()
        for client in clients:
            if client["addr"] == addr_input:
                try:
                    client["conn"].send(f"f:{file_name}".encode(FORMAT))
                    time.sleep(0.1)
                    client["conn"].send(data.encode(FORMAT))
                except BrokenPipeError:
                    print_msg(f"[ERROR] Cannot send file to {addr_input}")
                break
        else:
            print_msg(f"[ERROR] Cannot send file to {addr_input}")
            


def main():
    print_msg("[STARTING] Server is starting...")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)
    server.listen()
    print_msg(f"[LISTENING] Server is listening on {IP}:{PORT}")

    send_thread = threading.Thread(target=send_file)
    send_thread.start()

    print_msg(f"[ACTIVE CONNECTIONS] {threading.active_count() - 2}")

    while True:
        conn, addr = server.accept()
        clients.append({"conn": conn, "addr": addr})
        thread = threading.Thread(target=handle_client, args=(conn,addr))
        thread.start()
        print_msg(f"[ACTIVE CONNECTIONS] {threading.active_count() - 2}")

if __name__=="__main__":
    main()