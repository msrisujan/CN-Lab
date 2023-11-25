import socket
import threading
IP = socket.gethostbyname(socket.gethostname())
PORT = 5577
ADDR = (IP, PORT)
SIZE = 1024
DISCONNECT_MESSAGE = "!DISCONNECT"

clients_conn = {}
def find_name(name):
    for i in clients_conn:
        if i == name:
            return clients_conn[i]
def check(conn,name):
    print(f"New connection {name} connected")
    while True:
        msg = conn.recv(SIZE).decode()
        print(msg)
        conn_list = find_name(name)
        k = 0
        print(conn_list)
        if msg == "s0":
            for j in range(0, len(conn_list)):
                print(conn_list[j])
                if conn_list[j] == "s1":
                    conn.send("d:s2,s3".encode())
                    if "s2" in clients_conn[name]:
                        clients_conn[name].remove("s2")
                    if "s3" in clients_conn[name]:
                        clients_conn[name].remove("s3")
                    k = 1
                    break
                elif conn_list[j] == "s4":
                    conn.send("d:all".encode())
                    clients_conn[name] = []
                    k = 1
                    break
                
            if k != 1:
                conn.send("OK:s0".encode())
            clients_conn[name].append("s0")
        elif msg == "s1":
            if len(conn_list) != 0 and conn_list[0] == "s0":
                conn.send("NO:s1".encode())
            else:
                conn.send("OK:s1".encode())
                clients_conn[name].append("s1")
        elif msg == "s2":
            if len(conn_list) != 0 and conn_list[0] == "s0":
                conn.send("NO:s2".encode())
            else:
                conn.send("OK:s2".encode())
                clients_conn[name].append("s2")
        elif msg == "s3":
            if len(conn_list) != 0 and conn_list[0] == "s0":
                conn.send("NO:s3".encode())
            else:
                conn.send("OK:s3".encode())
                clients_conn[name].append("s3")
        elif msg == "s4":
            if len(conn_list) != 0 and conn_list[0] == "s0":
                conn.send("NO:s4".encode())
                k = 1
            for i in conn_list:
                if i == "s1":
                    conn.send("NO:s4".encode())
                    k = 1
            if k != 1:
                conn.send("OK:s4".encode())
                clients_conn[name].append("s4")
        else:
            s = msg.split(':')[1]
            clients_conn[name].remove(s)


def main():
    print("[STARTING] Server is starting...")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)
    server.listen()
    print(f"[LISTENING] Server is listening on {IP}:{PORT}")

    while True:
        conn, addr = server.accept()
        name = conn.recv(SIZE).decode()
        clients_conn[name] = []
        thread = threading.Thread(target=check, args=(conn,name))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")

if __name__=="__main__":
    main()