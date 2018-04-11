from math import e, pow
import matplotlib.pyplot as plt
import numpy as np


# Variant 12:
# f(x, y) = dy/dx = x*y^2 + 3 * x * y

def __exactY(x, c):
    """
        x: current x value
        c: precalculated c value equal to c = y0 / (pow(e, 1.5 * x0 * x0) * (3 + y0))
    """
    tmp = pow(e, 1.5 * x * x)
    return 3 * c * tmp / (1 - c * tmp)


def exactGraph(x0, X, steps, f=None, y0=None):
    c = y0 / (pow(e, 1.5 * x0 * x0) * (3 + y0))

    x = np.linspace(x0, X, steps)
    values = {'x': x, 'y': [y0]}

    h = (X - x0) / float(steps)
    for i in x[1:]:
        # Handle 0 devision
        try:
            y = __exactY(i, c)
            i += h
            values['y'].append(y)
        except ZeroDivisionError:
            print("Zero division occurred. Function is chunky!")
    return values


def errorGraph(values, prepared_exacts=None):
    """
    :param values: dictionary where 'x' and 'y' arrays stored
    :return: dictionary with local error values and x values
    """
    x = values['x']
    y = values['y']
    x0 = x[0]
    X = x[-1]
    steps = len(x)
    y0 = y[0]
    errors = []
    # exacts = []
    # if prepared_exacts == None:
    #     exacts = exactGraph(x0, X, steps, y0=y0)['y']
    # else:
    #     exacts = prepared_exacts['y']
    exacts = exactGraph(x0, X, steps, y0=y0)['y'] if prepared_exacts == None else prepared_exacts['y']
    for i, ex in enumerate(exacts):
        errors.append(abs(ex - y[i]))
    return {'x': x, 'y': errors}


# TODO: remove tests
if __name__ == "__main__":
    print("Exact algorithm testing executing...")

    d = exactGraph(-1.5, 8.5, 10000, y0=-2.0)
    # print(len(d['x']), d['x'])
    # print(len(d['y']), d['y'])
    plt.plot(d['x'], d['y'])
    plt.show()
