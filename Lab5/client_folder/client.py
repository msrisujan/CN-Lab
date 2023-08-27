import socket
import threading
import readline
import time

IP = socket.gethostbyname(socket.gethostname())
PORT = 5566
ADDR = (IP, PORT)
SIZE = 1024
FORMAT = "utf-8"
DISCONNECT_MSG = "!DISCONNECT"

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
        file_name = conn.recv(SIZE).decode(FORMAT)
        if file_name == DISCONNECT_MSG:
            connected = False
            print_msg(f"[DISCONNECTED] {addr} disconnected.")
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
                print_msg(f"[SERVER]: {msg}")

            else:
                print_msg(f"[ERROR] Unknown message type: {msg_type}")
    conn.close()

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)
    print_msg(f"[CONNECTED] Client connected to {IP}:{PORT}")

    receive_file_thread = threading.Thread(target=receive_file, args=(client,ADDR))
    receive_file_thread.start()

    connected = True
    while connected:
        file_name = input_msg("Enter the file name: ")
        if file_name == DISCONNECT_MSG:
            client.send(file_name.encode(FORMAT))
            connected = False
            break
        client.send(f"f:{file_name}".encode(FORMAT))
                
        time.sleep(0.1)
        
        file = open(file_name,"r")
        data = file.read()
        client.send(data.encode(FORMAT))
        
        file.close()
    client.close()

if __name__=="__main__":
    main()