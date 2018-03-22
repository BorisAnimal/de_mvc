def rk(x0, X, steps, f=None, y0=None):
    values = {'x': [x0], 'y': [y0]}
    x = x0
    y = y0
    h = (X - x0) / float(steps)
    hh = h / 2  # half of h
    for i in range(steps):
        try:
            k1 = f(x, y)
            k2 = f(x + hh, y + hh * k1)
            k3 = f(x + hh, y + hh * k2)
            k4 = f(x + h, y + h * k3)
            y = y + h / 6 * (k1 + 2 * (k2 + k3) + k4)
            x = x + h
            values['y'].append(y)
            values['x'].append(x)
        except ZeroDivisionError:
            print("Zero division occurred. Function is chunky!")
    return values

# # TODO: remove tests
# if __name__ == "__main__":
#     print("Euler's algorithm testing executing...")
#
#
#     def func(x, y):
#         return 2 * x
#
#
#     d = (rk(func, 5.0, 0.0, 5.0, 25))
#     print(len(d['x']), d['x'])
#     print(len(d['y']), d['y'])
