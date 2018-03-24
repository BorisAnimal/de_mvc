from eulerAlgorithm import improved_euler, euler
from rangeKuttaAlgorithm import rk
from exactAlgorithm import exactGraph
from enum import Enum


class Selector(Enum):
    EULER = 'euler',
    IMP_EULER = 'imp_euler',
    RUNGE_KUTTA = 'rk',
    EXACT = 'exact'


def derivative(x, y):
    return y * (float(x) * y + 3.0 * x)


class Filter:
    # Keeps state and input information of system
    def __init__(self):
        # Inputs
        self.x0 = 3 / 4.0
        self.y0 = 3.0
        self.X = 5.5
        self.N = 100
        self.selected_method = Selector.EULER

        # Implementated
        self.methods = {Selector.EULER: euler,
                        Selector.IMP_EULER: improved_euler,
                        Selector.RUNGE_KUTTA: rk,
                        Selector.EXACT: exactGraph}

    def get_data(self):
        return self.methods[self.selected_method](x0=self.x0, X=self.X, steps=self.N, f=derivative, y0=self.y0)

    def get_error(self):
        pass

    def __str__(self):
        return "x0: {}\ny0: {}\nX: {}\nN: {}\nMethod: {}".format(str(self.x0), str(self.y0), str(self.X), str(self.N), self.selected_method )





