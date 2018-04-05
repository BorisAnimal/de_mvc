from math import e, pow
import matplotlib.pyplot as plt


# Variant 12:
# f(x, y) = dy/dx = x*y^2 + 3 * x * y

def __exactY(X, c):
    x = float(X)
    return c * pow(e, 1.5 * x * x) / (1 - c * pow(e, 1.5 * x * x))


def exactGraph(x0, X, steps, f=None, y0=None):
    x = x0
    c = y0 / (pow(e, 1.5 * x0 * x0) * (1 + y0))
    values = {'x': [], 'y': []}
    h = (X - x0) / float(steps)
    for i in range(steps):
        # Handle 0 devision
        try:
            y = __exactY(x, c)
            x += h
            values['y'].append(y)
            values['x'].append(x)
        except ZeroDivisionError:
            print("Zero division occurred. Function is chunky!")
    return values


# TODO: remove tests
if __name__ == "__main__":
    print("Exact algorithm testing executing...")

    d = exactGraph(-5.0, 15.0, 1000, y0=0.05)
    # print(len(d['x']), d['x'])
    # print(len(d['y']), d['y'])
    plt.plot(d['x'], d['y'])
    plt.show()
