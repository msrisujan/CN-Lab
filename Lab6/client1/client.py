# Lab 6: Write a Socket Program or extend the earlier text file transfer program from any one client to another client which support following file transfers.

# 1. MS Word file
# 2. SOffice file
# 3. PDF 
# 4. Image
# 5. video and any other file format of document.

#client.py

import socket
import readline
import threading
import time

IP = socket.gethostbyname(socket.gethostname())
PORT = 5567
ADDR = (IP, PORT)
SIZE = 1024
DISCONNECT_MESSAGE = "!DISCONNECT"

current_input = ""

def print_msg(msg):
    input_buffer = readline.get_line_buffer()
    print(f"\r{msg}\n{current_input}{input_buffer}",end="",flush=True)

def input_msg(input_str):
    global current_input
    current_input = input_str
    output = input(f"\r{input_str}")
    return output

def receive_file(conn,addr):
    connected = True
    while connected:
        file_name = conn.recv(SIZE).decode()

        type = file_name.split(":")[0]
        file = file_name.split(":")[1]
        if type == "a":
            print_msg(f"[SERVER] {file}")
            continue

        if type == "l":
            print_msg(f"{file}")
            continue

        with open(f"received_{file}", "wb") as f:
            print_msg(f"[RECEIVING] Receiving {file}...")
            data = conn.recv(SIZE)
            while data != b"EOF":
                f.write(data)
                data = conn.recv(SIZE)
            print_msg(f"[RECEIVED] {file} received.")
            conn.send("a:[RECEIVED] ".encode())
            f.close()
            
        
    conn.close()

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)
    print_msg(f"[CONNECTED] Client connected to {IP}:{PORT}")

    receive_file_thread = threading.Thread(target=receive_file, args=(client,ADDR))
    receive_file_thread.start()

    while True:
        msg = input_msg("(IP PORT):")
        if msg == DISCONNECT_MESSAGE:
            print_msg(f"[DISCONNECTED] Disconnected from {IP}:{PORT}")
            client.send(msg.encode())
            break
        else:
            client.send(msg.encode())
        file_name = input_msg("File name:")
        client.send(f"f:{file_name}".encode())

        with open(file_name, "rb") as f:
            print_msg(f"[SENDING] Sending {file_name}...")
            while True:
                data = f.read(SIZE)
                if not data:
                    break
                client.send(data)
            time.sleep(0.1)
            client.send(b"EOF")
            print_msg(f"[SENT] {file_name} sent.")
            f.close()

    client.close()

if __name__ == "__main__":
    main()