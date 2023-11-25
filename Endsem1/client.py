import socket
import threading
import readline
IP = socket.gethostbyname(socket.gethostname())
PORT = 5577
PORT0 = 1234
PORT1 = 2345
PORT2 = 3456
PORT3 = 4567
PORT4 = 5678
ADDR = (IP, PORT)
ADDR0 = (IP, PORT0)
ADDR1 = (IP, PORT1)
ADDR2 = (IP, PORT2)
ADDR3 = (IP, PORT3)
ADDR4 = (IP, PORT4)
SIZE = 1024
DISCONNECT_MESSAGE = "!DISCONNECT"

current_input = ""
connected = []
def print_msg(msg):
    input_buffer = readline.get_line_buffer()
    print(f"\r{msg}\n{current_input}{input_buffer}",end="",flush=True)

def input_msg(input_str):
    global current_input
    current_input = input_str
    output = input(f"\r{input_str}")
    return output

s0 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s3 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s4 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
def recieve_msg(client):
    while True:
        msg = client.recv(SIZE).decode()
        type = msg.split(':')[0]
        if type == "d":
            dis = msg.split(':')[1]
            if dis == "all":
                for i in connected:
                    if i == "s1":
                        s1.send(DISCONNECT_MESSAGE.encode())
                        print_msg("Disconnected from s1")
                    if i == "s2":
                        s2.send(DISCONNECT_MESSAGE.encode())
                        print_msg("Disconnected from s2")
                    if i == "s3":
                        s3.send(DISCONNECT_MESSAGE.encode())
                        print_msg("Disconnected from s3")
                    if i == "s4":
                        s4.send(DISCONNECT_MESSAGE.encode())
                        print_msg("Disconnected from s4")
                s0.connect(ADDR0)
                connected.append("s0")
                print_msg("Connected to s0")
            else:
                for i in connected:
                    if i == "s2":
                        s2.send(DISCONNECT_MESSAGE.encode())
                        print_msg("Disconnected from s2")
                    if i == "s3":
                        s3.send(DISCONNECT_MESSAGE.encode())
                        print_msg("Disconnected from s3")
                s0.connect(ADDR0)
                connected.append("s0")
                print_msg("Connected to s0")
        elif type == "NO":
            server = msg.split(':')[1]
            print_msg("Not able to connnect")
        else:
            server = msg.split(':')[1]
            if server == "s0":
                s0.connect(ADDR0)
                connected.append("s0")
                print_msg("Connected to s0")
            if server == "s1":
                s1.connect(ADDR1)
                connected.append("s1")
                print_msg("Connected to s1")
            if server == "s2":
                s2.connect(ADDR2)
                connected.append("s2")
                print_msg("Connected to s2")
            if server == "s3":
                s3.connect(ADDR3)
                connected.append("s3")
                print_msg("Connected to s3")
            if server == "s4":
                s4.connect(ADDR4)
                connected.append("s4")
                print_msg("Connected to s4")



def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)
    name = input_msg("Enter name: ")
    client.send(name.encode())
    connected1 = True
    while connected1:
        
        print_msg("1.connect to server")
        print_msg("2.disconnect from server")
        choice = input_msg("Enter choice: ")
        server = input_msg("Enter Server: ")
        receive_thread = threading.Thread(target=recieve_msg, args=(client,))
        receive_thread.start()
        if choice == "1":
            client.send(server.encode())
        if choice == "2":
            client.send(f"d:{server}".encode())
            for i in connected:
                if i == server:
                    if i == "s0":
                        s0.send(DISCONNECT_MESSAGE.encode())
                        print_msg("Disconnected from s0")
                    if i == "s1":
                        s1.send(DISCONNECT_MESSAGE.encode())
                        print_msg("Disconnected from s1")
                    if i == "s2":
                        s2.send(DISCONNECT_MESSAGE.encode())
                        print_msg("Disconnected from s2")
                    if i == "s3":
                        s3.send(DISCONNECT_MESSAGE.encode())
                        print_msg("Disconnected from s3")
                    if i == "s4":
                        s4.send(DISCONNECT_MESSAGE.encode())
                        print_msg("Disconnected from s4")
            else:
                print_msg("You are not connected to that server")


if __name__=="__main__":
    main()