from models.Environment import Enviorment
from utils.map_utils import *
from models.maps import q_map
from models.Environment import Enviorment
import pygame
import random

COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)
COLOR_GREY = (46, 46, 46)
COLOR_BLUE = (0, 200, 255)
COLOR_DARK_GREY = (169, 160, 181)
COLOR_GREEN = (144, 238, 144)
COLOR_RED = (255, 69, 0)
PIXEL_SIZE = 10
WIDTH_POSITION = len(q_map[0]) * PIXEL_SIZE
HEIGHT_POSITION = len(q_map) * PIXEL_SIZE

enviorment = Enviorment()
pygame.init()
screen = pygame.display.set_mode((WIDTH_POSITION, HEIGHT_POSITION))
pygame.display.set_caption('Q-Learning')
screen.fill(COLOR_WHITE)
clock = pygame.time.Clock()


def first_render_screen():
    for y in range(0, len(q_map[0])):
        for x in range(0, len(q_map)):
            pos_x = x * PIXEL_SIZE
            pos_y = y * PIXEL_SIZE
            if q_map[y][x] == 1:
                pygame.draw.rect(screen, COLOR_GREY,
                                 (pos_x, pos_y, PIXEL_SIZE, PIXEL_SIZE))
    pygame.display.update()


def exit_game():
    pygame.display.quit()
    pygame.quit()
    exit()


def printar_mapa():
    for y in range(0, len(q_map[0])):
        for x in range(0, len(q_map)):
            print(q_map[y][x], end=" ")
        print()


def pygame_start_game():
    x = y = 0
    while q_map[y][x] != 0:
        x = random.randint(1, len(q_map[0]) - 1)
        y = random.randint(1, len(q_map) - 1)
        print(x, y)
    q_map[y][x] = 2
    first_render_screen()
    running = True
    while running:
        # clock.tick(60)
        decision = enviorment.states[y][x].actions[random.randint(
            0, len(enviorment.states[y][x].actions) - 1)]
        if decision.action == 'up':
            q_map[y][x] = 0
            pygame.draw.rect(
                screen, COLOR_WHITE, (x*PIXEL_SIZE, y*PIXEL_SIZE, PIXEL_SIZE, PIXEL_SIZE))
            y -= 1
            q_map[y][x] = 2
            pygame.draw.rect(
                screen, COLOR_BLUE, (x*PIXEL_SIZE, y*PIXEL_SIZE, PIXEL_SIZE, PIXEL_SIZE))

        elif decision.action == 'down':
            q_map[y][x] = 0
            pygame.draw.rect(
                screen, COLOR_WHITE, (x*PIXEL_SIZE, y*PIXEL_SIZE, PIXEL_SIZE, PIXEL_SIZE))
            y += 1
            q_map[y][x] = 2
            pygame.draw.rect(
                screen, COLOR_BLUE, (x*PIXEL_SIZE, y*PIXEL_SIZE, PIXEL_SIZE, PIXEL_SIZE))
        elif decision.action == 'left':
            q_map[y][x] = 0
            pygame.draw.rect(
                screen, COLOR_WHITE, (x*PIXEL_SIZE, y*PIXEL_SIZE, PIXEL_SIZE, PIXEL_SIZE))
            x -= 1
            q_map[y][x] = 2
            pygame.draw.rect(
                screen, COLOR_BLUE, (x*PIXEL_SIZE, y*PIXEL_SIZE, PIXEL_SIZE, PIXEL_SIZE))
        elif decision.action == 'right':
            q_map[y][x] = 0
            pygame.draw.rect(
                screen, COLOR_WHITE, (x*PIXEL_SIZE, y*PIXEL_SIZE, PIXEL_SIZE, PIXEL_SIZE))
            x += 1
            q_map[y][x] = 2
            pygame.draw.rect(
                screen, COLOR_BLUE, (x*PIXEL_SIZE, y*PIXEL_SIZE, PIXEL_SIZE, PIXEL_SIZE))
        
        if y == 0 and x == 29:
            running = False
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game()
