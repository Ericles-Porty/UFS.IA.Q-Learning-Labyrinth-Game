from os import environ
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

def generate_random_pos():
    x = y = 0
    while q_map[y][x] != 0:
        x = random.randint(1, len(q_map[0]) - 1)
        y = random.randint(1, len(q_map) - 1)
    return x, y

def draw(x,y,color):
    pygame.draw.rect(screen, color, (x*PIXEL_SIZE, y*PIXEL_SIZE, PIXEL_SIZE, PIXEL_SIZE))

def pygame_start_game():
    x = y = steps = 0
    x,y = generate_random_pos()
    q_map[y][x] = 2
    first_render_screen()
    running = True
    while running:
        # clock.tick(60)
        decision_index = random.randint(
            0, len(enviorment.states[y][x].actions) - 1)
        decision = enviorment.states[y][x].actions[decision_index]
        if decision.q > 0:
            print("Q: ", decision.q)
            q_map[y][x] = 0
            draw(x,y,COLOR_WHITE)
            if decision.action == "up":
                enviorment.states[y][x].actions[decision_index].q = enviorment.calc_q(0.9, enviorment.states[y][x].r, enviorment.get_max(y-1,x))
                y -= 1
            elif decision.action == "down":
                enviorment.states[y][x].actions[decision_index].q = enviorment.calc_q(0.9, enviorment.states[y][x].r, enviorment.get_max(y+1,x))
                y += 1
            elif decision.action == "left":
                enviorment.states[y][x].actions[decision_index].q = enviorment.calc_q(0.9, enviorment.states[y][x].r, enviorment.get_max(y,x-1))
                x -= 1
            elif decision.action == "right":
                enviorment.states[y][x].actions[decision_index].q = enviorment.calc_q(0.9, enviorment.states[y][x].r, enviorment.get_max(y,x+1))
                x += 1
            q_map[y][x] = 2
            draw(x,y,COLOR_BLUE)
            pygame.display.update()
        else:
            if decision.action == 'up':
                q_map[y][x] = 0
                draw(x,y,COLOR_WHITE)
                y -= 1
                q_map[y][x] = 2
                draw(x,y,COLOR_BLUE)

            elif decision.action == 'down':
                q_map[y][x] = 0
                draw(x,y,COLOR_WHITE)
                y += 1
                q_map[y][x] = 2
                draw(x,y,COLOR_BLUE)
            elif decision.action == 'left':
                q_map[y][x] = 0
                draw(x,y,COLOR_WHITE)
                x -= 1
                q_map[y][x] = 2
                draw(x,y,COLOR_BLUE)
            elif decision.action == 'right':
                q_map[y][x] = 0
                draw(x,y,COLOR_WHITE)
                x += 1
                q_map[y][x] = 2
                draw(x,y,COLOR_BLUE)
            steps += 1
            if y == 0 and x == 29:
                print("Chegou ao fim em {} passos".format(steps))
                q_map[y][x] = 0
                pygame.draw.rect(
                    screen, COLOR_WHITE, (x*PIXEL_SIZE, y*PIXEL_SIZE, PIXEL_SIZE, PIXEL_SIZE))
                x,y = generate_random_pos()
                q_map[y][x] = 2
                pygame.draw.rect(
                    screen, COLOR_BLUE, (x*PIXEL_SIZE, y*PIXEL_SIZE, PIXEL_SIZE, PIXEL_SIZE))
                steps = 0
                # running = False
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game()
