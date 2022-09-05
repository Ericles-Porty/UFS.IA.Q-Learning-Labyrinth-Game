import numpy as np
from .Cell import *
from .maps import *
from utils import *

class Bot():
    def __init__(self, pos_x: int, pos_y: int):
        self.pos_x = pos_x
        self.pos_y = pos_y

    def reset(self):
        self.pos_x = 0
        self.pos_y = 0