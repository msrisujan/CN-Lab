import socket

s = socket.socket()

port = 57001

s.connect(('192.168.137.121', port))

print(s.recv(1024).decode())

s.close()