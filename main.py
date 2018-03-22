#!/usr/bin/env python
# -*- coding:utf-8 -*-

# TODO: fix chunks in funciton

import random
import sys

from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

from filter import Selector
from controller import *

from PyQt4 import QtGui, QtCore


class MatplotlibWidget(QtGui.QWidget):
    """
    Widget on view with graphics
    """

    def __init__(self, parent=None):
        super(MatplotlibWidget, self).__init__(parent)

        self.figure = Figure()
        self.canvas = FigureCanvasQTAgg(self.figure)

        self.axis = self.figure.add_subplot(111)

        self.layoutVertical = QtGui.QVBoxLayout(self)
        self.layoutVertical.addWidget(self.canvas)


class ThreadSample(QtCore.QThread):
    """
    Class that provides data to graph (@MatplotlibWidget)
    """
    newSample = QtCore.pyqtSignal(list)

    def __init__(self, parent=None):
        super(ThreadSample, self).__init__(parent)

    def run(self):
        # TODO: ask controller for new data
        randomSample = random.sample(range(0, 1000), 100)

        self.newSample.emit(randomSample)


class MyWindow(QtGui.QWidget):
    """
    View enter point (GUI)
    """

    def __init__(self, parent=None):
        super(MyWindow, self).__init__(parent)

        self.controller = Controller()

        self.solutionGraphWidget = MatplotlibWidget(self)
        self.errorGraphWidget = MatplotlibWidget(self)

        # Main layout (horizontal)
        self.hbox = QtGui.QHBoxLayout(self)
        self.hbox.addStretch(1)
        # Left control panel layout (vertical)
        self.control_box = QtGui.QVBoxLayout(self)
        self.hbox.addLayout(self.control_box)

        # init views
        self.x0Edit = QtGui.QLineEdit()
        self.y0Edit = QtGui.QLineEdit()
        self.XEdit = QtGui.QLineEdit()
        self.notificationsEdit = QtGui.QTextEdit()
        self.notificationsEdit.setEnabled(False)
        self.NEdit = QtGui.QLineEdit()
        self.exactButton = QtGui.QPushButton("Exact")
        self.eulerButton = QtGui.QPushButton("Euler")
        self.eulerImpButton = QtGui.QPushButton("ImprovedEuler")
        self.rkButton = QtGui.QPushButton("Runge Kutta")

        # Control panel composition
        grid = QtGui.QGridLayout()
        grid.setSpacing(18)

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

        grid.addWidget(self.notificationsEdit, 10, 0, 1, 2)

        self.control_box.addLayout(grid)

        # init graph's layout
        rgrid = QtGui.QGridLayout()
        rgrid.setSpacing(2)
        rgrid.addWidget(self.solutionGraphWidget)
        rgrid.addWidget(self.errorGraphWidget)
        self.hbox.addLayout(rgrid)

        self.exactButton.clicked.connect(lambda: self.on_algorithmButton_clicked(selector=Selector.EXACT))
        self.eulerButton.clicked.connect(lambda: self.on_algorithmButton_clicked(selector=Selector.EULER))
        self.eulerImpButton.clicked.connect(lambda: self.on_algorithmButton_clicked(selector=Selector.IMP_EULER))
        self.rkButton.clicked.connect(lambda: self.on_algorithmButton_clicked(selector=Selector.RUNGE_KUTTA))

        self.threadSample = ThreadSample(self)
        self.threadSample.newSample.connect(self.on_threadSample_newSample)
        self.threadSample.finished.connect(self.on_threadSample_finished)
        self.update_state()

    def update_state(self):
        self.solutionGraphWidget.axis.clear()

    @QtCore.pyqtSlot()
    def on_algorithmButton_clicked(self, selector):
        self.controller.filter.selected_method = selector
        self.solutionGraphWidget.axis.clear()
        self.threadSample.start()

    @QtCore.pyqtSlot(list)
    def on_threadSample_newSample(self, sample):
        self.solutionGraphWidget.axis.plot(sample)
        self.solutionGraphWidget.canvas.draw()

    @QtCore.pyqtSlot()
    def on_threadSample_finished(self):
        self.threadSample.start()


if __name__ == "__main__":
    import sys

    app = QtGui.QApplication(sys.argv)
    app.setApplicationName('Differential Equations')

    main = MyWindow()
    main.resize(1000, 800)
    main.show()

    sys.exit(app.exec_())
