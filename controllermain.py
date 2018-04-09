from eulerAlgorithm import improved_euler, euler
from rangeKuttaAlgorithm import rk
from exactAlgorithm import exactGraph, errorGraph
from enum import Enum



class Selector(Enum):
    EULER = 'Euler',
    IMP_EULER = 'Improved_euler',
    RUNGE_KUTTA = 'Runge_Kutta',
    EXACT = 'Exact'


class ControllerMain:
    ALG_CLR = {Selector.EULER: 'g', Selector.IMP_EULER: 'r', Selector.RUNGE_KUTTA: 'b', Selector.EXACT: 'w'}

    # Keeps state and input information of system
    def __init__(self, view):
        self.view = view
        # Inputs
        self.x0 = -2.0
        self.y0 = -2.0
        self.X = 8.5
        self.N = 100
        self.selected_methods = []
        self.derivative = lambda x, y: y * (float(x) * y + 3.0 * x) #min(9999999.0, y * (float(x) * y + 3.0 * x))

        # Approximation and exact algorithm methods
        self.methods = {Selector.EULER: euler,
                        Selector.IMP_EULER: improved_euler,
                        Selector.RUNGE_KUTTA: rk,
                        Selector.EXACT: exactGraph}

    def update_view(self):
        res = self.get_data()
        self.view.clear_graphs()
        for i, values in enumerate(res):
            sel = self.selected_methods[i]
            self.view.plot_solution(values['x'], values['y'], self.ALG_CLR[sel], sel.name)
            # Error graph
            err = self.get_error(values)
            self.view.plot_error(err['x'], err['y'], self.ALG_CLR[sel], sel.name)

    def switch_selector(self, selector):
        if selector not in self.selected_methods:
            self.selected_methods.append(selector)
        else:
            self.selected_methods.remove(selector)

    def set_x0(self, x0):
        self.x0 = float(x0)

    def set_y0(self, y0):
        self.y0 = float(y0)

    def set_X(self, X):
        self.X = X

    def set_N(self, N):
        self.N = int(N)

    def get_data(self):
        """
        :return: list of dictionaries with 'x' and 'y' lists!!!
        """
        data = []
        for i in self.selected_methods:
            data.append(self.methods[i](x0=self.x0, X=self.X, steps=self.N, f=self.derivative, y0=self.y0))
        return data

    def get_error(self, values):
        """
        :param values: dictionary with 'x' and 'y' only!!!
        :return:
        """
        return errorGraph(values)

    def __str__(self):
        return "x0: {}\ny0: {}\nX: {}\nN: {}\nMethod: {}".format(str(self.x0), str(self.y0), str(self.X),
                                                                 str(self.N),
                                                                 self.selected_methods)


class ControllerStepError:
    ALG_CLR = {Selector.EULER: 'g', Selector.IMP_EULER: 'r', Selector.RUNGE_KUTTA: 'b', Selector.EXACT: 'w'}

    # Keeps state and input information of system
    def __init__(self, view):
        self.view = view
        self.n0 = 40
        self.N = 100
        self.selected_methods = []

    def switch_selector(self, selector):
        if selector not in self.selected_methods:
            self.selected_methods.append(selector)
        else:
            self.selected_methods.remove(selector)



if __name__ == "__main__":
    controller = ControllerMain(None)
    # Test #1: graphs
    # print("Algorithm testing executing...")
    # import matplotlib.pyplot as plt
    #
    # d = controller.get_data()
    # print(d['y'])
    # plt.plot(d['y'])
    # plt.ylabel('some numbers')
    # plt.show()

    # Test #2: selectors switching
    print(controller.selected_methods)
    print("Append:")
    controller.switch_selector(Selector.EXACT)
    controller.switch_selector(Selector.RUNGE_KUTTA)
    print(controller.selected_methods)
    print("Remove 'rk':")
    controller.switch_selector(Selector.RUNGE_KUTTA)
    print(controller.selected_methods)
