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
PIXEL_SIZE = 20
WIDTH_POSITION = len(q_map[0]) * PIXEL_SIZE
HEIGHT_POSITION = len(q_map) * PIXEL_SIZE
Y_GOAL = 6
X_GOAL = 6

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
    steps = 0
    while running:
        # clock.tick(60)
        best_index_action = enviorment.best_index_action(x, y)
        if enviorment.states[y][x].actions[best_index_action].q == 0:
            decision_index = random.randint(0, len(enviorment.states[y][x].actions) - 1)
            decision = enviorment.states[y][x].actions[decision_index] 
            # print("Random decision")          
        else:
            decision_index = best_index_action
            decision = enviorment.states[y][x].actions[decision_index]
            print("Q: ", decision.q)
        # for i in range(0, len(enviorment.states[y][x].actions)):
        #     print(enviorment.states[y][x].actions[i].action, end=" - ")
        # print()
        # print("Best: ", decision.action)
        # print("| Action: ",enviorment.states[y][x].actions[best_index_action].action, "Index: " ,best_index_action)
        # print("Y: ",y,"X: ", x, enviorment.states[y][x].actions[decision_index].q)

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
        steps += 1
        if y == Y_GOAL and x == X_GOAL:
            print("Chegou ao fim em {} passos".format(steps))
            q_map[y][x] = 0
            draw(x,y,COLOR_WHITE)
            x,y = generate_random_pos()
            q_map[y][x] = 2
            draw(x,y,COLOR_BLUE)
            steps = 0
            # running = False
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                for i in range(0, len(enviorment.states)):
                    for j in range(0, len(enviorment.states[i])):
                        for k in range(0, len(enviorment.states[i][j].actions)):
                            if enviorment.states[i][j].actions[k].q != 0:
                                with open("q.txt",'a') as f:
                                    f.write(str(i)+','+str(j)+','+str(enviorment.states[i][j].actions[k].q)+","+str(enviorment.states[i][j].actions[k].action)+'\n')
                                print("Q: ",i, j, enviorment.states[i][j].actions[k].q,enviorment.states[i][j].actions[k].action)
                exit_game()
