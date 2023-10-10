# Lab 6: Write a Socket Program or extend the earlier text file transfer program from any one client to another client which support following file transfers.

# 1. MS Word file
# 2. SOffice file
# 3. PDF 
# 4. Image
# 5. video and any other file  of document.

#server.py
import socket
import readline
import threading
import time

IP = socket.gethostbyname(socket.gethostname())
PORT = 5566
ADDR = (IP, PORT)
SIZE = 1024
DISCONNECT_MESSAGE = "!DISCONNECT"

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

def send_msg(addrs,msg):
    for client in clients:
        if client["addr"] == addrs:
            client["conn"].send(msg.encode())
            break


def send_file(conn, addr):
    print_msg(f"[NEW CONNECTION] {addr} connected.")
    for client in clients:
        if client["addr"] != addr:
            conn.send(f"l:({client['addr'][0]} {client['addr'][1]}) connected to server".encode())
    for client in clients:
        if client["addr"] != addr:
            client["conn"].send(f"l:({addr[0]} {addr[1]}) connected to server".encode())


    connected = True
    while connected:

        ip_port = conn.recv(SIZE).decode()
        if not ip_port:
            continue

        if ip_port == DISCONNECT_MESSAGE:
            connected = False
            for client in clients:
                if client["addr"] != addr:
                    client["conn"].send(f"l:({addr[0]} {addr[1]}) disconnected from server".encode())
            for client in clients:
                if client["addr"] == addr:
                    clients.remove(client)
                    break
            else:
                print_msg(f"[ERROR] Cannot disconnect {addr}")
            print_msg(f"\r[DISCONNECT CONNECTION] {addr} disconnected.")
            print_msg(f"[ACTIVE CONNECTIONS] {threading.active_count() - 2}")
            break
        
        addrs =(ip_port.split(' ')[0], int(ip_port.split(' ')[1]))

        for client in clients:
            if client["addr"] == addrs:
                break
        else:
            conn.send(f"e: {addrs} not found.".encode())
            continue
        
        file_name = conn.recv(SIZE).decode()
        send_msg(addrs,file_name)

        for client in clients:
            if client["addr"] == addrs:
                send_conn = client["conn"]

        data = conn.recv(SIZE)
        while data != b"EOF":
            send_conn.send(data)
            data = conn.recv(SIZE)
        time.sleep(0.1)
        send_conn.send(b"EOF")
        conn.send("a:[SENT] File sent.".encode())
        ack = send_conn.recv(SIZE).decode()
        conn.send(f"{ack} by {addrs}".encode())
    conn.close()

def main():
    print_msg("[STARTING] Server is starting...")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)
    server.listen()
    print_msg(f"[LISTENING] Server is listening on {IP}:{PORT}")

    while True:
        conn, addr = server.accept()
        clients.append({"addr":addr, "conn":conn})
        thread = threading.Thread(target=send_file, args=(conn,addr))
        thread.start()
        print_msg(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")

if __name__=="__main__":
    main()
