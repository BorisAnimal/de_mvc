from math import e, pow
import matplotlib.pyplot as plt


# Variant 12:
# f(x, y) = dy/dx = x*y^2 + 3 * x * y

def __exactY(X, c):
    x = float(X)
    return 3 * c * pow(e, 3 * x * x / 2) / (1 - c * pow(e, 3 * x * x / 2))


def exactGraph(x0, X, steps, f=None, y0=None):
    x = x0
    c = y0 / (y0 + 3) * pow(e, 3 * x0 * x0 / 2)
    y = __exactY(x0, c)
    values = {'x': [x0], 'y': [y]}
    h = (X - x0) / float(steps)
    for i in range(steps):
        # Handle 0 devision
        try:
            y = __exactY(x, c)
            x = x + h
            values['y'].append(y)
            values['x'].append(x)
        except ZeroDivisionError:
            print("Zero division occurred. Function is chunky!")
    return values


# TODO: remove tests
if __name__ == "__main__":
    print("Euler's algorithm testing executing...")

    d = exactGraph(0.0, 5.5, 200, y0=3)
    print(len(d['x']), d['x'])
    print(len(d['y']), d['y'])
    plt.plot(d['x'], d['y'])
    plt.show()
