import numpy as np

def improved_euler(x0, X, steps, f=None, y0=None):
    return __basic(f, y0, x0, X, steps, __imp_eul_lambda)


def euler(x0, X, steps, f=None, y0=None):
    return __basic(f, y0, x0, X, steps, __eul_lambda)


def __basic(f, y0, x0, X, steps, alg):
    values = {'x': [x0], 'y': [y0]}
    x = x0
    y = y0
    h = (X - x0) / float(steps)

    for i in range(steps):
        try:
            y = alg(f, x, y, h)
            x = x + h
            values['y'].append(y)
            values['x'].append(x)
        except ZeroDivisionError:
            print("Zero division occurred. Function is chunky!")
    return values


def __imp_eul_lambda(f, x, y, h):
    return y + (f(x, y) + f(x + h, y + h * f(x, y))) / 2 * h


def __eul_lambda(f, x, y, h):
    return y + f(x, y) * h

# # TODO: remove tests
# if __name__ == "__main__":
#     print("Euler's algorithm testing executing...")
#
#
#     def func(x, y):
#         return 2 * x
#
#
#     d = (improved_euler(func, 5.0, 0.0, 5.0, 25))
#     print(len(d['x']), d['x'])
#     print(len(d['y']), d['y'])
