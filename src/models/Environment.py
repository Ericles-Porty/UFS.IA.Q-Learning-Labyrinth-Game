from .States import States
from .Actions import Action
from .maps import q_map

FACTOR = 0.9


# if q_map[y-1][x] == 0:
#                     move_actions.append(
#                         Action("up", self.calc_q(FACTOR, 0, self.get_max(y-1, x))))
#                 if q_map[y+1][x] == 0:
#                     move_actions.append(
#                         Action("down", self.calc_q(FACTOR, 0, self.get_max(y+1, x))))
#                 if q_map[y][x-1] == 0:
#                     move_actions.append(
#                         Action("left", self.calc_q(FACTOR, 0, self.get_max(y, x-1))))
#                 if q_map[y][x+1] == 0:
#                     move_actions.append(
#                         Action("right", self.calc_q(FACTOR, 0, self.get_max(y, x+1))))

class Enviorment():
    def __init__(self):
        self.states = []
        self.q = []
        self.create_states()
        self.fill_actions()

    def fill_actions(self):
        for y in range(0, len(self.states)-1):
            for x in range(0, len(self.states[0])-1):
                for i in range(len(self.states[y][x].actions)):
                    if self.states[y][x].actions[i].action == "up":
                        self.states[y][x].actions[i].q = self.calc_q(
                            FACTOR, self.states[y][x].r, self.get_max(y-1, x))
                    if self.states[y][x].actions[i].action == "down":
                        self.states[y][x].actions[i].q = self.calc_q(
                            FACTOR, self.states[y][x].r, self.get_max(y+1, x))
                    if self.states[y][x].actions[i].action == "left":
                        self.states[y][x].actions[i].q = self.calc_q(
                            FACTOR, self.states[y][x].r, self.get_max(y, x-1))
                    if self.states[y][x].actions[i].action == "right":
                        self.states[y][x].actions[i].q = self.calc_q(
                            FACTOR, self.states[y][x].r, self.get_max(y, x+1))

    def create_states(self):
        for y in range(0, len(q_map[0])-1):
            temp_states = []
            for x in range(0, len(q_map)-1):
                move_actions = []
                # if q_map[y][x] == 0 and x % 2 == 1 and y % 2 == 1:
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
        self.states[0][29].r = 10 # goal = States(29, 0)

    def calc_q(self, factor: float, reward: float, max_q: float):
        return reward + factor * max_q

    def get_max(self, y, x) -> int:
        max = 0
        for i in range(len(self.states[y][x].actions)):
            if self.states[y][x].actions[i].q > max:
                max = self.states[y][x].actions[i].q
        return max

    def debug(self):
        for i in self.states:
            for l in i:
                print(l.x, l.y, end=' ')
                for j in l.actions:
                    print(j.action, j.q, end=' ')
                print()


new = Enviorment()
# new.states[47][53].actions[0].q = 1
# new.states[47][53].actions[1].q = 1
# new.states[47][53].actions[2].q = 1
# new.states[47][53].actions[3].q = 5
# print(new.get_max(47,53))
new.debug()
