#LABYTINTTIPELI
import pygame
import random
import numpy as np
import time

#asetukset
WIDTH, HEIGHT = 800,800 #ikkunan leveys ja koko pikseleinä
TITLE_SIZE = 20
TITLE = "Labyrinth"
VISIBLE_RADIUS = 5
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
font = pygame.font.Font(None, 36)


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
    

# aseta pelaajan ja itemit
def place_items(maze, count, goal):
    items = []
    while len(items) < count:
        x, y = random.randint(1, maze.shape[0] - 2), random.randint(1, maze.shape[1] - 2)
        if maze[x, y] == 0 and (x, y) not in items and (x, y) != goal:
            items.append((x, y))
    return items


# Piirrä labirintti
def draw_maze(maze,player_pos,items, goal_pos, elapsed_time):
    visible_radius = 3 # pelaajan näkyyvyden säde
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

  
    # Näytetään kulunut aika ja kerätyt esineet
    pygame.draw.rect(screen, BLACK, (0, HEIGHT - 50, WIDTH, 50))  # tausta
    items_text = font.render(f"Esineitä jäljellä: {len(items)}", True, WHITE)
    time_text = font.render(f"Aika: {elapsed_time:.2f} s", True, WHITE)
    screen.blit(items_text, (10, HEIGHT - 70))
    screen.blit(time_text, (10, HEIGHT - 40))



# PELI
def game():
    while True:
        maze = generate_maze(31, 31)  # Generoi labyrintti
        player_pos = [1, 1]  # Pelaajan aloituspaikka
        goal = (29, 29)  # Maali alue
        items = place_items(maze, 5, goal)  # Aseta esineet
        start_time = time.time()
        running = True

        while running:
            elapsed_time = time.time() - start_time

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
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

            if not items and tuple(player_pos) == goal:
                print("Peli loppui!")
                print(f"Aikaa kului: {time.time() - start_time:.2f} sekuntia")
                running = False

            draw_maze(maze, player_pos, items, goal, elapsed_time)  # Päivitä labyrintti
            pygame.display.flip()  # Päivitä näyttö
            clock.tick(FPS)

        pygame.time.wait(1000)
        screen.fill(BLACK)
        end_text = font.render("Peli päättyi! ENTER = Uudestaan, ESC = Lopeta", True, WHITE)
        screen.blit(end_text, (WIDTH // 2 - end_text.get_width() // 2, HEIGHT // 2 - end_text.get_height() // 2))
        pygame.display.flip()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        waiting = False
                    elif event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        return

game()