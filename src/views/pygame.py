from models.Environment import Enviorment, Y_GOAL, X_GOAL, FACTOR
from models.maps import q_map, question
import random

extract_mode = int(input("Quer importar os dados do aprendizado anterior? (1 - Sim | 0 - Não): "))
save_mode = False
if extract_mode == False:
    save_mode = int(input("Quer salvar os dados do aprendizado ao final? (1 - Sim | 0 - Não): "))
debug_mode = int(input("Quer ver o debug? (1 - Sim | 0 - Não): "))
game_mode = int(input("Quer ver a interface gráfica? (1 - Sim | 0 - Não): "))

COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)
COLOR_GREY = (46, 46, 46)
COLOR_BLUE = (0, 200, 255)
COLOR_DARK_GREY = (169, 160, 181)
COLOR_GREEN = (144, 238, 144)
COLOR_PURE_GREEN = (0, 255, 0)
COLOR_RED = (255, 69, 0)
if question == 1:
    PIXEL_SIZE = 60
else:
    PIXEL_SIZE = 15
WIDTH_POSITION = len(q_map[0]) * PIXEL_SIZE
HEIGHT_POSITION = len(q_map) * PIXEL_SIZE

running = True
enviorment = Enviorment()

if game_mode:
    import pygame
    pygame.init()
    screen = pygame.display.set_mode((WIDTH_POSITION, HEIGHT_POSITION))
    pygame.display.set_caption('Q-Learning-Labyrinth')
    screen.fill(COLOR_WHITE)
    # clock = pygame.time.Clock()


def pygame_start_game():
    if game_mode:
        first_render_screen()    
    
    if extract_mode:
        enviorment.extract_q(question)
    if game_mode:
        q_learning_pygame()
    else:
        q_learning()


def save_q():
    print("Salvando tabela Q")
    with open("q.csv",'w') as f:
        f.write('y;'+'x;'+'q;'+'action\n')
    for i in range(0, len(enviorment.states)):
        for j in range(0, len(enviorment.states[i])):
            for k in range(0, len(enviorment.states[i][j].actions)):
                if enviorment.states[i][j].actions[k].q != 0:
                    with open('q.csv','a') as f:
                        f.write(str(i)+';'+str(j)+';'+str(enviorment.states[i][j].actions[k].q)+';'+str(enviorment.states[i][j].actions[k].action)+'\n')
                    if debug_mode:
                        print("Q: ",i, j, enviorment.states[i][j].actions[k].q,enviorment.states[i][j].actions[k].action)
    print("Tabela Q salva com sucesso!")

def first_render_screen():
    for y in range(0, len(q_map[0])):
        for x in range(0, len(q_map)):
            pos_x = x * PIXEL_SIZE
            pos_y = y * PIXEL_SIZE
            if y == Y_GOAL and x == X_GOAL:
                draw(x,y,COLOR_PURE_GREEN)
            if q_map[y][x] == 1:
                pygame.draw.rect(screen, COLOR_GREY,
                                 (pos_x, pos_y, PIXEL_SIZE, PIXEL_SIZE))


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
    while q_map[y][x] != 0 or (x == X_GOAL and y == Y_GOAL):
        x = random.randint(1, len(q_map[0]) - 1)
        y = random.randint(1, len(q_map) - 1)
    return x, y


def draw(x,y,color):
    pygame.draw.rect(screen, color, (x*PIXEL_SIZE, y*PIXEL_SIZE, PIXEL_SIZE, PIXEL_SIZE))


def q_learning_pygame():
    x = y = 0
    x,y = generate_random_pos()
    q_map[y][x] = 2
    steps = 0
    counter = 0
    while running:
        if counter >= 15000:
            verifica_convergencia()
            counter = 0
        counter += 1
        pygame.display.update()
        # clock.tick(120)
        best_index_action = enviorment.best_index_action(x, y)
        if enviorment.states[y][x].actions[best_index_action].q == 0:
            decision_index = random.randint(0, len(enviorment.states[y][x].actions) - 1)
            decision = enviorment.states[y][x].actions[decision_index] 
            q_map[y][x] = 0
            draw(x,y,COLOR_WHITE)
        else:
            decision_index = best_index_action
            decision = enviorment.states[y][x].actions[decision_index]
            if debug_mode:
                print("Q: ", decision.q , "Action: ", decision.action, "X: ", x, "Y: ", y)
            q_map[y][x] = 0
            draw(x,y,(0,int(decision.q*25),0))

        
        if decision.action == "up":
            enviorment.states[y][x].actions[decision_index].q = enviorment.calc_q(FACTOR, enviorment.states[y-1][x].r, enviorment.get_max(y-1,x))
            y -= 1

        elif decision.action == "down":
            enviorment.states[y][x].actions[decision_index].q = enviorment.calc_q(FACTOR, enviorment.states[y+1][x].r, enviorment.get_max(y+1,x))
            y += 1

        elif decision.action == "left":
            enviorment.states[y][x].actions[decision_index].q = enviorment.calc_q(FACTOR, enviorment.states[y][x-1].r, enviorment.get_max(y,x-1))
            x -= 1

        elif decision.action == "right":
            enviorment.states[y][x].actions[decision_index].q = enviorment.calc_q(FACTOR, enviorment.states[y][x+1].r, enviorment.get_max(y,x+1))
            x += 1
            
        q_map[y][x] = 2
        draw(x,y,COLOR_BLUE)
        steps += 1
        if y == Y_GOAL and x == X_GOAL:
            if debug_mode:
                print("Chegou ao fim em {} passos".format(steps))
            q_map[y][x] = 0
            draw(x,y,COLOR_PURE_GREEN)
            x,y = generate_random_pos()
            q_map[y][x] = 2
            draw(x,y,COLOR_BLUE)
            steps = 0
        events = pygame.event.get()
        for event in events:                     
            if event.type != pygame.QUIT:
                pass
            else:
                exit_game()
    return

def q_learning():
    x = y = 0
    x,y = generate_random_pos()
    q_map[y][x] = 2
    running = True
    steps = 0
    counter = 0
    while running:
        if counter >= 1500:
            verifica_convergencia()
            counter = 0
        counter += 1

        best_index_action = enviorment.best_index_action(x, y)
        if enviorment.states[y][x].actions[best_index_action].q == 0:
            decision_index = random.randint(0, len(enviorment.states[y][x].actions) - 1)
            decision = enviorment.states[y][x].actions[decision_index] 
            q_map[y][x] = 0
        else:
            decision_index = best_index_action
            decision = enviorment.states[y][x].actions[decision_index]
            if debug_mode:
                print("Q: ", decision.q , "Action: ", decision.action, "X: ", x, "Y: ", y)
            q_map[y][x] = 0

        
        if decision.action == "up":
            enviorment.states[y][x].actions[decision_index].q = enviorment.calc_q(FACTOR, enviorment.states[y-1][x].r, enviorment.get_max(y-1,x))
            y -= 1

        elif decision.action == "down":
            enviorment.states[y][x].actions[decision_index].q = enviorment.calc_q(FACTOR, enviorment.states[y+1][x].r, enviorment.get_max(y+1,x))
            y += 1

        elif decision.action == "left":
            enviorment.states[y][x].actions[decision_index].q = enviorment.calc_q(FACTOR, enviorment.states[y][x-1].r, enviorment.get_max(y,x-1))
            x -= 1

        elif decision.action == "right":
            enviorment.states[y][x].actions[decision_index].q = enviorment.calc_q(FACTOR, enviorment.states[y][x+1].r, enviorment.get_max(y,x+1))
            x += 1
            
        q_map[y][x] = 2
        steps += 1
        if y == Y_GOAL and x == X_GOAL:
            if debug_mode:
                print("Chegou ao fim em {} passos".format(steps))
            q_map[y][x] = 0
            x,y = generate_random_pos()
            q_map[y][x] = 2
            steps = 0
    return
        
def verifica_convergencia():
    counter = 0
    for i in range(len(q_map)-1):
        for j in range(len(q_map[i])-1):
            if q_map[i][j] == 0:
                if enviorment.get_max(i,j) == 0:
                    counter += 1
    if counter == 1:
        print("Aprendeu")
        if save_mode:
            global running
            running = False
            save_q()
            exit()
    else:
        print("Ainda não aprendeu! Quantidade restante para aprender:",counter)