import socket
import threading
import readline
IP = socket.gethostbyname(socket.gethostname())

PORT = 6677
PORT0 = 4321
PORT1 = 5432
ADDR = (IP, PORT)
ADDR0 = (IP, PORT0)
ADDR1 = (IP, PORT1)
SIZE = 1024
DISCONNECT_MESSAGE = "!DISCONNECT"


current_input = ""
connection = 0
def print_msg(msg):
    input_buffer = readline.get_line_buffer()
    print(f"\r{msg}\n{current_input}{input_buffer}",end="",flush=True)

def input_msg(input_str):
    global current_input
    current_input = input_str
    output = input(f"\r{input_str}")
    return output




def main():
    global connection
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)
    
    connected = True
    while connected:
        print_msg("1.connect")
        print_msg("2.disconnect")
        choice = input_msg("Enter choice: ")
        if choice == "1":
            S = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            receive_thread = threading.Thread(target=recieve_msg, args=(client,S))
            receive_thread.start()
            msg = "connect"
            client.send(msg.encode())
        else:
            S.send(DISCONNECT_MESSAGE.encode())
            if connection == 0:
                print_msg("Disconnected from S")

            else:
                print_msg("Disconnected from Sr")

def recieve_msg(client,S):
    global connection
    while True:
        msg = client.recv(SIZE).decode()
        if msg == "OK":
            S.connect(ADDR0)
            print_msg("Connected to S")
        else:
            S.connect(ADDR1)
            connection = 1
            print_msg("Connected to Sr")

if __name__=="__main__":
    main()