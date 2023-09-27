import socket
import threading
import os
import pygame
from pong4 import *

IP = socket.gethostbyname(socket.gethostname())
PORT = 53531
ADDR = (IP, PORT)
SIZE = 1024
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "DISCONNECT!"

player_num = 0
player_pos = {
    1: "Left",
    2: "Right",
    3: "Top",
    4: "Bottom"
}
    

def disconnect(conn):
    conn.send(DISCONNECT_MESSAGE.encode(FORMAT))
    print(f"[DISCONNECTED] Disconnected from {ADDR}")
    conn.close()
    os._exit(0)

def update_game_state(conn):
    global player_num,player_pos
    while True:
        conn.send("GET;".encode(FORMAT))
        msg = conn.recv(SIZE).decode(FORMAT)
        msg = msg.split("}")[0] + "}"
        gs = GameState.from_json(msg)

        screen.fill(BLACK)

        drawscore(screen, font, gs.H, gs.FourPlayers, gs)
        screen.blit(font.render(f"Player - {player_num} ({player_pos[player_num]}) ", True, WHITE), (gs.W//2-35,35))
        drawball(screen, gs.bx, gs.by, gs.bw)

        drawpaddle(screen, gs.p1x, gs.p1y, gs.paddle_width_v, gs.paddle_height_v, py1_Color) 
        drawpaddle(screen, gs.p2x, gs.p2y, gs.paddle_width_v, gs.paddle_height_v, py2_Color)

        if gs.FourPlayers:
            drawpaddle(screen, gs.p3x, gs.p3y, gs.paddle_width_h, gs.paddle_height_h, py3_Color)
            drawpaddle(screen, gs.p4x, gs.p4y, gs.paddle_width_h, gs.paddle_height_h, py4_Color)

        pygame.display.flip()

        if gs.winner != 0:
            screen.fill(BLACK)
            screen.blit(font.render(f"{pl[gs.winner]} Player wins!", True, WHITE), (gs.W//2-100,gs.H//2-50))
            if gs.winner == player_num:
                screen.blit(font.render(f"You win!", True, WHITE), (gs.W//2-100,gs.H//2))
            else:
                screen.blit(font.render(f"You lose!", True, WHITE), (gs.W//2-100,gs.H//2))
            pygame.display.flip()
            break




def main():
    global player_num
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)
    print(f"[CONNECTED] Connected to {ADDR}")
    msg_confirm = client.recv(SIZE).decode(FORMAT)
    if(msg_confirm == DISCONNECT_MESSAGE):
        disconnect(client)
    player_num = int(msg_confirm)
    print(f"[ASSIGNED] Assigned player number {player_num}")

    #display waiting screen
    screen = pygame.display.set_mode((gs.W, gs.H))
    pygame.display.set_caption("Pong")
    font = pygame.font.SysFont("Arial", 30)
    screen.fill(BLACK)
    screen.blit(font.render(f"Waiting for other players...", True, WHITE), (gs.W//2-150,gs.H//2-50))
    pygame.display.flip()

    game_started = client.recv(SIZE).decode(FORMAT)
    if game_started == "START":
        print(f"[START] Game started!")
    else:
        print(f"[ERROR] Game did not start!")
        return
    
    #display starting game in 3 seconds
    for i in range(3,0,-1):
        screen.fill(BLACK)
        screen.blit(font.render(f"Starting game in {i}...", True, WHITE), (gs.W//2-100,gs.H//2-50))
        pygame.display.flip()
        pygame.time.wait(1000)
    
    game_thread = threading.Thread(target=update_game_state, args=(client,))
    game_thread.start()
    
    connected = True
    while connected:
        key_map = {
            pygame.K_w: "up",
            pygame.K_s: "down",
            pygame.K_UP: "up",
            pygame.K_DOWN: "down",
            pygame.K_a: "left",
            pygame.K_d: "right",
            pygame.K_LEFT: "left",
            pygame.K_RIGHT: "right"
        }
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                connected = False
                # pygame.quit()
                disconnect(client)
                break
            if event.type == pygame.KEYDOWN:
                if event.key in key_map:
                    msg = f"KEYDOWN:{key_map[event.key]};"
                    client.send(msg.encode(FORMAT))
            if event.type == pygame.KEYUP:
                if event.key in key_map:
                    msg = f"KEYUP:{key_map[event.key]};"
                    client.send(msg.encode(FORMAT))
    client.close()

if __name__ == "__main__":
    main()