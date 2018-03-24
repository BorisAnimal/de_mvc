from filter import *


class Controller():

    def __init__(self):
        self.filter = Filter()

    def set_x0(self, x0):
        self.filter.x0 = float(x0)

    def set_y0(self, y0):
        self.filter.y0 = float(y0)

    def set_X(self, X):
        self.filter.X = X

    def set_N(self, N):
        self.filter.N = N
