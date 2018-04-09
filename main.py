#!/usr/bin/env python
# -*- coding:utf-8 -*-

from PyQt5 import QtGui, QtCore
import pyqtgraph as pg
from controllers import *


class MyWindow(QtGui.QWidget):
    """
    View enter point (GUI)
    """

    def __init__(self, parent=None):
        super(MyWindow, self).__init__(parent)

        self.controller = ControllerMain(self)
        self.init_components()
        self.init_controllpanel()
        self.init_graphs()

        self.exactButton.clicked.connect(lambda: self.on_algorithmButton_clicked(selector=Selector.EXACT))
        self.eulerButton.clicked.connect(lambda: self.on_algorithmButton_clicked(selector=Selector.EULER))
        self.eulerImpButton.clicked.connect(lambda: self.on_algorithmButton_clicked(selector=Selector.IMP_EULER))
        self.rkButton.clicked.connect(lambda: self.on_algorithmButton_clicked(selector=Selector.RUNGE_KUTTA))

        self.changeStateButton.clicked.connect(self.changeState)

        self.x0Edit.valueChanged.connect(self.update_state)
        self.y0Edit.valueChanged.connect(self.update_state)
        self.NEdit.valueChanged.connect(self.update_state)
        self.XEdit.valueChanged.connect(self.update_state)

        self.update_state()

    def changeState(self):
        print("change")
        self.dialog = Second(self)
        # self.dialog.show()
        self.dialog.exec_()

    def init_graphs(self):
        # init graph's layout
        rgrid = QtGui.QGridLayout()
        rgrid.setSpacing(2)
        rgrid.addWidget(self.solutionGraphWidget)
        rgrid.addWidget(self.errorGraphWidget)
        self.hbox.addLayout(rgrid)

    def init_controllpanel(self):
        # Control panel composition
        grid = QtGui.QGridLayout()
        grid.setSpacing(20)

        grid.addWidget(QtGui.QLabel('Initial'), 0, 0)
        grid.addWidget(QtGui.QLabel('Conditions'), 0, 1)

        grid.addWidget(QtGui.QLabel('x0'), 2, 0)
        grid.addWidget(self.x0Edit, 2, 1)

        grid.addWidget(QtGui.QLabel('y0'), 3, 0)
        grid.addWidget(self.y0Edit, 3, 1)

        grid.addWidget(QtGui.QLabel('X'), 4, 0)
        grid.addWidget(self.XEdit, 4, 1)

        grid.addWidget(QtGui.QLabel('N'), 5, 0)
        grid.addWidget(self.NEdit, 5, 1)

        grid.addWidget(self.exactButton, 6, 0, 1, 2)  # int fromRow, int fromColumn, int rowSpan, int columnSpan
        grid.addWidget(self.eulerButton, 7, 0, 1, 2)
        grid.addWidget(self.eulerImpButton, 8, 0, 1, 2)
        grid.addWidget(self.rkButton, 9, 0, 1, 2)
        grid.addWidget(self.changeStateButton, 10, 0, 1, 2)

        grid.addWidget(self.notificationsEdit, 11, 0, 1, 2)
        self.control_box.addLayout(grid)

    def init_components(self):
        self.solutionGraphWidget = pg.PlotWidget(self, name='Solutions')
        self.errorGraphWidget = pg.PlotWidget(self, name='Errors')

        # Main layout (horizontal)
        self.hbox = QtGui.QHBoxLayout(self)
        # Left control panel layout (vertical)
        self.control_box = QtGui.QVBoxLayout(self)
        self.hbox.addLayout(self.control_box, 0)

        # init views
        self.x0Edit = QtGui.QDoubleSpinBox(minimum=-4.5, maximum=3.5, value=self.controller.x0)
        self.y0Edit = QtGui.QDoubleSpinBox(minimum=-2.99, maximum=0.0,
                                           value=self.controller.y0)  # (minimum=-4.99, maximum=3.0, value=-2.0)
        self.XEdit = QtGui.QDoubleSpinBox(minimum=-3.5, maximum=5.5, value=self.controller.X)
        self.notificationsEdit = QtGui.QTextEdit()
        self.notificationsEdit.setEnabled(False)
        self.NEdit = QtGui.QSpinBox(minimum=40, maximum=10000, value=self.controller.N)  # TODO: write this in report
        # Select method(s)
        self.exactButton = QtGui.QCheckBox("Exact")
        self.eulerButton = QtGui.QCheckBox("Euler")
        self.eulerImpButton = QtGui.QCheckBox("ImprovedEuler")
        self.rkButton = QtGui.QCheckBox("Runge-Kutta")
        self.changeStateButton = QtGui.QPushButton("Max Error>>")

    def log(self, s):
        print(s)
        self.notificationsEdit.insertPlainText(str(s))
        self.notificationsEdit.moveCursor(QtGui.QTextCursor.End)

    def update_state(self):
        print("update")
        self.controller.set_x0(self.x0Edit.value())
        self.controller.set_y0(self.y0Edit.value())
        self.controller.set_X(self.XEdit.value())
        self.controller.set_N(int(self.NEdit.value()))
        self.XEdit.setMinimum(self.x0Edit.value() + 1.0)
        self.controller.update_view()

    @QtCore.pyqtSlot()
    def on_algorithmButton_clicked(self, selector):
        try:
            self.controller.switch_selector(selector)
            self.update_state()
        except:
            self.log("Exception accured (1)!\n")

    def plot_solution(self, x, y, clr, legend):
        self.solutionGraphWidget.plot(x, y, pen=clr, name=legend)

    def plot_error(self, x, y, clr, legend):
        self.errorGraphWidget.plot(x, y, pen=clr, name=legend)

    def clear_graphs(self):
        try:
            self.solutionGraphWidget.clear()
            self.solutionGraphWidget.getViewBox().removeItem(self.solutionGraphWidget.plotItem.legend)
            self.solutionGraphWidget.addLegend()
            self.errorGraphWidget.clear()
            self.errorGraphWidget.getViewBox().removeItem(self.errorGraphWidget.plotItem.legend)
            self.errorGraphWidget.addLegend()  # offset = 200
        except:
            self.log("Exception accured (2)!!!\n")


class Second(QtGui.QDialog):
    def __init__(self, parent=None):
        super(Second, self).__init__(parent)
        self.controller = ControllerStepError(self, tmp=parent.controller)
        self.init_components()
        self.n0Edit.valueChanged.connect(self.update_state)
        self.NEdit.valueChanged.connect(self.update_state)
        self.eulerButton.clicked.connect(lambda: self.on_algorithmButton_clicked(selector=Selector.EULER))
        self.improvedEulerButton.clicked.connect(lambda: self.on_algorithmButton_clicked(selector=Selector.IMP_EULER))
        self.rkButton.clicked.connect(lambda: self.on_algorithmButton_clicked(selector=Selector.RUNGE_KUTTA))
        self.updateButton.clicked.connect(self.on_updateButton_clicked)

        self.resize(500, 600)


    def clear_graphs(self):
        try:
            self.stepErrorGraphWidget.clear()
            self.stepErrorGraphWidget.getViewBox().removeItem(self.stepErrorGraphWidget.plotItem.legend)
            self.stepErrorGraphWidget.addLegend()
        except:
            self.log("Exception accured (2)!!!\n")


    def plot_stepError(self, x, y, clr, legend):
        # print(x)
        # print(y)
        print(len(x))
        print(len(y))
        self.stepErrorGraphWidget.plot(x, y, pen=clr, name=legend)

    @QtCore.pyqtSlot()
    def on_updateButton_clicked(self):
        print("update (redraw)")
        self.controller.update_view()


    @QtCore.pyqtSlot()
    def on_algorithmButton_clicked(self, selector):
        try:
            print("Update selector")
            self.controller.switch_selector(selector)
        except:
            self.log("Exception accured (1)!\n")

    def update_state(self):
        print("update state")
        self.controller.N = int(self.NEdit.value())
        self.controller.n0 = int(self.n0Edit.value())
    
    def init_components(self):
        # Main layout (vertical)
        self.vbox = QtGui.QVBoxLayout(self)
        # Graph widget
        self.stepErrorGraphWidget = pg.PlotWidget(self, name='Step<->Error')
        self.vbox.addWidget(self.stepErrorGraphWidget)
        #Grid for control panel
        grid = QtGui.QGridLayout()
        grid.setSpacing(20)
        grid.addWidget(QtGui.QLabel('Parameters'), 0, 0, 1, 2)
        # n0
        grid.addWidget(QtGui.QLabel('n0'), 1, 0)
        self.n0Edit = QtGui.QSpinBox(minimum=40, maximum=960, value=self.controller.n0)
        grid.addWidget(self.n0Edit, 1, 1)
        # N 
        grid.addWidget(QtGui.QLabel('N'), 2, 0)
        self.NEdit = QtGui.QSpinBox(minimum=100, maximum=1000, value=self.controller.N)
        grid.addWidget(self.NEdit, 2, 1)
        # Algorithm checkbox
        self.eulerButton = QtGui.QCheckBox("Euler")
        self.improvedEulerButton = QtGui.QCheckBox("ImprovedEuler")
        self.rkButton = QtGui.QCheckBox("Runge-Kutta")
        grid.addWidget(self.eulerButton, 3, 0, 1, 2) 
        grid.addWidget(self.improvedEulerButton, 4, 0, 1, 2) 
        grid.addWidget(self.rkButton, 5, 0, 1, 2)
        # Update button
        self.updateButton = QtGui.QPushButton("Update")
        grid.addWidget(self.updateButton, 6, 0, 1, 2)
        self.vbox.addLayout(grid)


if __name__ == "__main__":
    import sys

    app = QtGui.QApplication(sys.argv)
    app.setApplicationName('Differential Equations')

    main = MyWindow()
    main.resize(1000, 800)
    main.show()

    sys.exit(app.exec_())
