import numpy as np
import matplotlib.pyplot as plt


def rk(x0, X, steps, f=None, y0=None):
    """
        Calculates the runge_kutt algorithm for given values
        :param x0: initial x
        :param y0: initial y
        :param f: derivative function
        :param X: right boreder of x axis
        :param steps: number of steps in approximation
        :return: dictionary with values 'x': [list of x axis values], 'y': [list of y axis values]
    """
    y = y0
    h = (X - x0) / float(steps)
    hh = h / 2  # half of h

    x = np.linspace(x0, X, steps)
    values = {'x': x, 'y': [y0]}
    for i in x[1:]:
        try:
            k1 = f(i, y)
            k2 = f(i + hh, y + hh * k1)
            k3 = f(i + hh, y + hh * k2)
            k4 = f(i + h, y + h * k3)
            y = y + h / 6 * (k1 + 2 * (k2 + k3) + k4)
            values['y'].append(y)
        except ZeroDivisionError:
            print("Zero division occurred. Function is chunky!")
    return values


# TODO: remove tests
if __name__ == "__main__":
    print("Euler's algorithm testing executing...")


    def func(x, y):
        return y * (float(x) * y + 3.0 * x)


    d = rk(0.5, 8.0, 1000, func, -0.5)
    print(len(d['x']))
    print(len(d['y']))
