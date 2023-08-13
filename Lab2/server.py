import socket

s = socket.socket()

port = 57001

s.bind(('', port))

s.listen(5)
print("Socket is listening...")

while True:
    c, addr = s.accept()
    print("Got connection from", addr)
    c.send("Thank you for connecting from sujan".encode())
    c.close()
    # break