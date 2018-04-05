#!/usr/bin/env python
# -*- coding:utf-8 -*-

import pyqtgraph as pg

from filter import Selector
from controller import *

from PyQt4 import QtGui, QtCore


class MyWindow(QtGui.QWidget):
    """
    View enter point (GUI)
    """

    def __init__(self, parent=None):
        super(MyWindow, self).__init__(parent)

        self.controller = Controller()

        self.solutionGraphWidget = pg.PlotWidget(self, name='Plot1')
        self.errorGraphWidget = pg.PlotWidget(self, name='Plot2')

        # Main layout (horizontal)
        self.hbox = QtGui.QHBoxLayout(self)
        # self.hbox.addStretch(1)
        # Left control panel layout (vertical)
        self.control_box = QtGui.QVBoxLayout(self)
        self.hbox.addLayout(self.control_box, 0)

        # init views
        self.x0Edit = QtGui.QDoubleSpinBox(minimum=3.0 / 4, maximum=90)
        self.y0Edit = QtGui.QDoubleSpinBox(minimum=-50, maximum=100)
        self.XEdit = QtGui.QDoubleSpinBox(minimum=5.0)
        self.notificationsEdit = QtGui.QTextEdit()
        self.notificationsEdit.setEnabled(False)
        self.NEdit = QtGui.QDoubleSpinBox(minimum=100, maximum=10000)  # TODO: write this in report
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
        # add control_box layout

        self.exactButton.clicked.connect(lambda: self.on_algorithmButton_clicked(selector=Selector.EXACT))
        self.eulerButton.clicked.connect(lambda: self.on_algorithmButton_clicked(selector=Selector.EULER))
        self.eulerImpButton.clicked.connect(lambda: self.on_algorithmButton_clicked(selector=Selector.IMP_EULER))
        self.rkButton.clicked.connect(lambda: self.on_algorithmButton_clicked(selector=Selector.RUNGE_KUTTA))
        self.x0Edit.valueChanged.connect(self.update_state)
        self.y0Edit.valueChanged.connect(self.update_state)
        self.NEdit.valueChanged.connect(self.update_state)
        self.XEdit.valueChanged.connect(self.update_state)

        self.update_state()

    def log(self, s):
        self.notificationsEdit.insertPlainText(s)
        self.notificationsEdit.moveCursor(QtGui.QTextCursor.End)

    def update_state(self):
        self.controller.set_x0(self.x0Edit.value())
        self.controller.set_y0(self.y0Edit.value())
        self.controller.set_X(self.XEdit.value())
        self.controller.set_N(int(self.NEdit.value()))

    @QtCore.pyqtSlot()
    def on_algorithmButton_clicked(self, selector):
        self.controller.filter.selected_method = selector
        self.solutionGraphWidget.clear()

        res = self.controller.filter.get_data()
        print(res)
        self.solutionGraphWidget.plot(res['x'], res['y'])


if __name__ == "__main__":
    import sys

    app = QtGui.QApplication(sys.argv)
    app.setApplicationName('Differential Equations')

    main = MyWindow()
    main.resize(1000, 800)
    main.show()

    sys.exit(app.exec_())
