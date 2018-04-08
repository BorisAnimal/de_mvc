import numpy as np
import matplotlib.pyplot as plt


def improved_euler(x0, X, steps, f=None, y0=None):
    return __basic(f, y0, x0, X, steps, __imp_eul_lambda)


def euler(x0, X, steps, f=None, y0=None):
    return __basic(f, y0, x0, X, steps, __eul_lambda)


def __basic(f, y0, x0, X, steps, alg):
    y = y0
    h = (X - x0) / float(steps)

    x = np.linspace(x0, X, steps)
    values = {'x': x, 'y': []}

    for i in x:
        try:
            y = alg(f, i, y, h)
            values['y'].append(y)
        except ZeroDivisionError:
            print("Zero division occurred. Function is chunky!")
    return values


def __imp_eul_lambda(f, x, y, h):
    return y + (f(x, y) + f(x + h, y + h * f(x, y))) / 2 * h


def __eul_lambda(f, x, y, h):
    # print(str(f(x, y)), x, y)
    return y + f(x, y) * h


# TODO: remove tests
if __name__ == "__main__":
    print("Euler's algorithm testing executing...")


    def func(x, y):
        return y * (float(x) * y + 3.0 * x)

    # 0.50, 8.0, 1000, y0=-0.5
    d = euler(0.5, 8.0, 1000, func, -0.5)
    print(len(d['y']))
    plt.plot(d['x'], d['y'])
    plt.ylabel('some numbers')
    plt.show()
