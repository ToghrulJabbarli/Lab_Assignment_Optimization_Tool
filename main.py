import sys
import numpy as np
import gurobipy as gp
import pandas as pd
from gurobipy import GRB
from PyQt5 import QtCore, QtWidgets
import qdarkstyle
from PyQt5.QtWidgets import *
import Window_Instructors


class Window(QtWidgets.QWidget):  # creating interface
    def __init__(self, listt, numberofi, v, numberofj):

        super().__init__()
        self.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
        self.list = listt
        self.numberofi = numberofi
        self.numberofj = numberofj
        self.v = v
        self.init_ui()

    def init_ui(self):
        # we create the widgets using in the interface
        v = self.v
        self.label2 = QtWidgets.QLabel("")
        self.buttonRun = QtWidgets.QPushButton("Run code")
        self.cb = []
        self.label = QtWidgets.QLabel("N:")
        self.tableWidget2 = QTableWidget()
        self.tableWidget2.setRowCount(self.numberofj)
        self.tableWidget2.setColumnCount(2)
        self.tableWidget2.setHorizontalHeaderLabels(["LAB", "DATE"])

        self.tableWidget = QTableWidget()
        self.tableWidget.setRowCount(self.numberofi)
        self.tableWidget.setColumnCount(1)
        self.tableWidget.setHorizontalHeaderLabels(["Instructor newcomer"])
        self.tableWidget.setVerticalHeaderLabels(self.list)
        for i in range(self.numberofi):
            self.cb.append(QCheckBox)

        self.textbox = QLineEdit(self)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch)

        self.tableWidget3 = QTableWidget()
        self.tableWidget3.setRowCount(self.numberofi)
        self.tableWidget3.setColumnCount(self.numberofj)
        self.tableWidget3.setVerticalHeaderLabels(self.list)

        # printing V matrix
        for i in range(self.tableWidget3.rowCount()):
            for j in range(self.tableWidget3.columnCount()):
                self.tableWidget3.setItem(i, j, QTableWidgetItem(str(v[i][j])))

        # designing layout and placing created widgets to interface
        self.item = []
        for i in range(self.numberofi):
            item = QtWidgets.QTableWidgetItem()
            item.setFlags(item.flags() | QtCore.Qt.ItemIsUserCheckable)
            item.setCheckState(QtCore.Qt.Unchecked)

            self.tableWidget.setItem(i, 0, item)
        h_box4 = QtWidgets.QHBoxLayout()

        h_box4.addWidget(self.label2)
        h_box = QtWidgets.QHBoxLayout()
        h_box.addWidget(self.buttonRun)

        h_box.addWidget(self.tableWidget2)

        h_box2 = QtWidgets.QHBoxLayout()

        h_box2.addWidget(self.tableWidget)
        # checking
        h_box2.addWidget(self.tableWidget3)

        h_box3 = QtWidgets.QHBoxLayout()
        h_box3.addWidget(self.label)
        h_box3.addWidget(self.textbox)

        v_box = QtWidgets.QVBoxLayout()
        v_box.addLayout(h_box4)
        v_box.addLayout(h_box)
        v_box.addLayout(h_box2)
        v_box.addLayout(h_box3)
        v_box.addStretch()

        self.setLayout(v_box)
        self.setWindowTitle("Lab Dates & Newcomers")
        self.setGeometry(600, 150, 700, 700)
        self.buttonRun.clicked.connect(self.click)
        self.show()

    # When we click the Run Button below lines will run
    def click(self):
        try:

            row = self.numberofi
            col = self.numberofj

            model = gp.Model("AssignmentQ1")

            # We create V matrix based on the number of instructors and labs
            v2 = np.zeros([self.tableWidget2.rowCount(),
                           self.tableWidget2.rowCount()])
            # if two different lab i and lab j are in same time slot, v2[i][j] matrix will be 1 for lab i and lab j
            column = []
            for i in range(self.tableWidget2.rowCount()):
                column.append(self.tableWidget2.item(i, 0).text() + self.tableWidget2.item(i, 1).text())
                for j in range(self.tableWidget2.rowCount()):
                    if i != j:
                        if self.tableWidget2.item(i, 1).text() == self.tableWidget2.item(j, 1).text():
                            v2[i][j] = 1

            v = self.v
            n = self.textbox.text()
            n = int(n)
            r = model.addVars(row, col, lb=0, vtype=GRB.INTEGER, name="r")

            # instuctor cannot be assigned to labs are in the same time slot
            for k in range(col):
                for m in range(col):
                    if v2[k][m] == 1:
                        constraint1 = model.addConstrs(r[i, k] + r[i, m] <= 1 for i in range(row))

            # each instructor can get maximum n labs
            constraint2 = model.addConstrs((gp.quicksum(r[i, j] for j in range(col)) <= n for i in range(row)),
                                           name='constraint2')
            # if lab instructor is newcomer .it will be provided by user
            for i in range(row):
                item = self.tableWidget.item(i, 0)

                if item.checkState() == QtCore.Qt.Checked:
                    constraint3 = model.addConstr(gp.quicksum(r[i, j] for j in range(col)) >= 1),

            # each lab has exactly 1 instructor
            constraint4 = model.addConstrs((gp.quicksum(r[i, j] for i in range(row)) == 1 for j in range(col)),
                                           name='constraint4')

            # After user manipulates cells new values are assigned to V matrix.
            for i in range(self.tableWidget3.rowCount()):
                for j in range(self.tableWidget3.rowCount()):
                    v[i][j] = self.tableWidget3.item(i, j).text()
            v.astype(int)

            # objective function
            model.setObjective(gp.quicksum(r[i, j] * v[i][j] for i in range(row) for j in range(col)), GRB.MAXIMIZE)
            # run model
            model.optimize()
            # print results
            result = np.zeros([row, col])
            for i in range(row):
                for j in range(col):
                    result[i, j] = r[i, j].x
                    print(f"\n  {r[i, j]} .")

            print(model.objVal)
            result = pd.DataFrame(result, columns=column, index=self.list)
            result.to_excel("output.xlsx")
            print(result)

            messagebox = QMessageBox()
            messagebox.setText("Assignment has been done.")
            messagebox.setWindowTitle("Warning")
            messagebox.setIcon(QMessageBox.Warning)
            messagebox.exec()
        except:
            messagebox = QMessageBox()
            messagebox.setText("Please check all data.")
            messagebox.setWindowTitle("Warning")
            messagebox.setIcon(QMessageBox.Warning)
            messagebox.exec()


if __name__=="__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Window_Instructors.Window2()
    sys.exit(app.exec_())


