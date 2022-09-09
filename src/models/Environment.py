from .States import States
from .Actions import Action
from .maps import q_map, question

import csv
if question == 1:
    X_GOAL = 6
    Y_GOAL = 6
    FACTOR=0.8
else:
    Y_GOAL = 0
    X_GOAL = 29
    FACTOR = 0.99

class Enviorment():
    def __init__(self):
        self.states = []
        self.q = []
        self.create_states()


    def get_index_by_action(self,y,x, action):
        for i in range(len(self.states[y][x].actions)):
            if self.states[y][x].actions[i].action == action:
                return i


    def extract_q(self,question):
        file = open(f'q{question}.csv')
        csvreader = csv.reader(file, delimiter=';')
        cont = 0
        for row in csvreader:
            if cont == 0:
                cont +=1
            else:
                y = int(row[0])
                x = int(row[1])
                q = float(row[2])
                action = row[3]
                self.states[y][x].actions[self.get_index_by_action(y,x,action)].q = q
        file.close()


    def create_states(self):
        for y in range(0, len(q_map[0])-1):
            temp_states = []
            for x in range(0, len(q_map)-1):
                move_actions = []
                if q_map[y-1][x] == 0:
                    move_actions.append(
                        Action("up", 0))
                if q_map[y+1][x] == 0:
                    move_actions.append(
                        Action("down", 0))
                if q_map[y][x-1] == 0:
                    move_actions.append(
                        Action("left", 0))
                if q_map[y][x+1] == 0:
                    move_actions.append(
                        Action("right", 0))
                temp_states.append(States(x, y, move_actions))
            self.states.append(temp_states)
        self.states[Y_GOAL][X_GOAL].r = 10 # goa


    def calc_q(self, factor: float, reward: float, max_q: float):
        return reward + factor * max_q


    def get_max(self, y, x) -> float:
        max = 0
        for i in range(len(self.states[y][x].actions)):
            if self.states[y][x].actions[i].q > max:
                max = self.states[y][x].actions[i].q
                # print("Max: ", max)
        return max


    def debug(self):
        for i in self.states:
            for l in i:
                print(l.x, l.y,l.r, end=' ')
                for j in l.actions:
                    print(j.action, j.q, end=' ')
                print()


    def best_index_action(self, x, y):
        max = 0
        index = 0
        for i in range(len(self.states[y][x].actions)):
            if self.states[y][x].actions[i].q >= max:
                index = i
                max = self.states[y][x].actions[i].q
        return  index
