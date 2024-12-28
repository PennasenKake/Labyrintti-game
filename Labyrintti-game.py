#LABYTINTTIPELI
import pygame
import random
import numpy as np
import time

#asetukset
WIDTH, HEIGHT = 1200, 800 #ikkunan leveys ja koko pikseleinä
TITLE_SIZE = 40
TITLE = "Labyrinth"
TITLE_COLOR = (255, 0, 0)
FPS = 60 #kuvataajuus

# värit
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

#Pygame alustus
pygame.init() # alustaa pygame kirjaston
screen = pygame.display.set_mode((WIDTH, HEIGHT)) # luo ikkunan jossa pelataan
pygame.display.set_caption(TITLE) #asettaa ikkunan otsikon
clock = pygame.time.Clock() # luodaan clock-olio joka laskee pelin kulkua varten

#labyrintin generointi
def generate_maze(width, height):
    # luo 2d-taulukon jossa on arvoja 1 (seinät). koko määritetaan parametrien avulla
    maze = np.ones((width, height), dtype=int)
    # pino jossa säilytetään solmujen sijainnit; aloitetaan koordinaatista (1, 1)
    stack = [(1,1)]
    # asetetaan alkuarvoon (1,1)
    maze[1,1] = 0
    direction = [(-2, 0), (2, 0), (0, -2), (0, 2)]

    while stack:
        x, y = stack[-1] # ota viimeinnen pinoelementti
        random.shuffle(direction) # sekoita liikkumissuunnat

        for dx, dy in direction:
            nx, ny = x + dx, y + dy
            # tarkistetaan, että uusi solmu on sijaintissa, joka on seinä
            if 1 <= nx < height - 1 and 1 <= ny < width - 1 and maze[nx, ny] == 1:
                maze[x + dx // 2, y + dy // 2] = 0 # poista seinä
                maze[nx, ny] = 0 # avaa seuraava solmu
                stack.append((nx, ny)) # lisää uuden solmun pinoon
                break
            # jos uusi solmu ei ole seinä, poistetaan sen pinoon
        else:
            stack.pop()

    maze[-2, -2] = 0 # maali
    return maze

# Piirrä labirintti
def draw_maze(maze,player_pos,items, goal_pos):
    visible_radius = 5 # pelaajan näkyyvyden säde
    px, py = player_pos
    screen.fill(BLACK) # täytä tausta mustanan
    
    for x in range(len(maze)):
        for y in range(len(maze[0])):
            if abs(px - x) <= visible_radius and abs(py - y) <= visible_radius:
                color = WHITE if maze[x][y] == 1 else BLACK
                pygame.draw.rect(screen, color, (y * TITLE_SIZE, x * TITLE_SIZE, TITLE_SIZE, TITLE_SIZE))

    for item in items:
        if maze[item[0], item[1]] == 0:
            pygame.draw.circle(screen, GREEN, (item[1] * TITLE_SIZE + TITLE_SIZE // 2, item[0] * TITLE_SIZE + TITLE_SIZE // 2), TITLE_SIZE // 4)
    
    # piirrä maali alue
    pygame.draw.rect(screen, RED, (goal_pos[1] * TITLE_SIZE, goal_pos[0] * TITLE_SIZE, TITLE_SIZE, TITLE_SIZE))

    # piirrä pelaaja
    pygame.draw.circle(screen, BLUE, (player_pos[1] * TITLE_SIZE + TITLE_SIZE // 2, player_pos[0] * TITLE_SIZE + TITLE_SIZE // 2), TITLE_SIZE // 3)


# PELI
def game():
    maze = generate_maze(21,21) # generoi 21x21 labyrintti
    player_pos = [1, 1] # pelaajan aloituspaikka
    items = [(random.randint(1, 19), random.randint(1, 19)) for _ in range(5)]  # Satunnaiset esineet
    goal = (19, 19) # maali alue
    start_time = time.time()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                new_pos = player_pos[:]
                if event.key == pygame.K_UP:
                    new_pos[0] -= 1
                elif event.key == pygame.K_DOWN:
                    new_pos[0] += 1
                elif event.key == pygame.K_LEFT:
                    new_pos[1] -= 1
                elif event.key == pygame.K_RIGHT:
                    new_pos[1] += 1
                if maze[new_pos[0]][new_pos[1]] == 0:
                    player_pos = new_pos


        items = [item for item in items if item != tuple(player_pos)]

        if tuple(player_pos) == goal:
            print("Peli loppui!")
            print(f"Aikaa kului: {time.time() - start_time:.2f} sekuntia")
            running = False

        draw_maze(maze, player_pos, items, goal) #päivitä labyrintti
        pygame.display.flip() # päivitä näyttö
        clock.tick(FPS)


game()
pygame.quit()