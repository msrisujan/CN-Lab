import socket
import threading
import os
import time
import pygame
from pong4 import *

# IP = socket.gethostbyname(socket.gethostname())
IP = ''
PORT = 53531
ADDR = (IP, PORT)
SIZE = 1024
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "DISCONNECT!"

clients = []


def assign_player():
    players = sorted([client["player"] for client in clients])
    num = 1
    for player in players:
        if player != num:
            return num
        num += 1
    return num

def handle_msg(conn, addr, player_num, msg):
    if msg == "GET":
        conn.send(gs.toJSON().encode(FORMAT))
    else:
        event_type, event_key = msg.split(":")
        player_map = {
            1: {
                "up": pygame.K_w,
                "down": pygame.K_s
            },
            2: {
                "up": pygame.K_UP,
                "down": pygame.K_DOWN
            },
            3: {
                "left": pygame.K_a,
                "right": pygame.K_d
            },
            4: {
                "left": pygame.K_LEFT,
                "right": pygame.K_RIGHT
            }
        }
        key_map = {
            "KEYDOWN": pygame.KEYDOWN,
            "KEYUP": pygame.KEYUP
        }
        # pygame.event.post(pygame.event.Event( key_map[event_type], key = player_map[player_num][event_key]))
        handle_movement(key_map[event_type], player_map[player_num][event_key])



def handle_client(conn, addr, player_num):
    print(f"[NEW CONNECTION] {addr} connected.")
    # for client in clients:
    #     if client["addr"] != addr:
    #         conn.send(f"l:({client['addr'][0]} {client['addr'][1]}) connected to server".encode())
    # for client in clients:
    #     if client["addr"] != addr:
    #         client["conn"].send(f"l:({addr[0]} {addr[1]}) connected to server".encode())

    connected = True
    while connected:
        msg = conn.recv(SIZE).decode(FORMAT)
        if msg == DISCONNECT_MESSAGE:
            connected = False
            print(f"[DISCONNECT] {addr} disconnected.")
            clients.remove({"addr":addr,"conn":conn, "player": player_num})
            break
        while ";" in msg:
            msg2, msg = msg.split(";",1)
            handle_msg(conn, addr, player_num, msg2)
            


    conn.close()



def main():
    game_thread = threading.Thread(target=game_loop)
    game_thread.start()
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)
    server.listen()
    print(f"[LISTENING] Server is listening on {IP}:{PORT}")
    print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 2}")
    game_started = False
    while True:
        conn, addr = server.accept()
        if((len(clients)==4 and gs.FourPlayers) or (len(clients)==2 and not gs.FourPlayers)):
            conn.send(DISCONNECT_MESSAGE.encode())
            continue
        player_num = assign_player()
        conn.send(f"{player_num}".encode())
        clients.append({"addr":addr,"conn":conn, "player": player_num})
        thread = threading.Thread(target=handle_client, args=(conn, addr, player_num))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 2}")

        if not game_started:
            if ((len(clients)==4 and gs.FourPlayers) or (len(clients)==2 and not gs.FourPlayers)):
                game_started = True
                for client in clients:
                    client["conn"].send("START".encode())

if __name__ == "__main__":
    main()