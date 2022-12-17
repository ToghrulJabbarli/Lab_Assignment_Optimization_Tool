import numpy as np
import qdarkstyle

from main import Window
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import *

class Window2(QtWidgets.QWidget):  # creating interface
    def __init__(self):

        super().__init__()
        self.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())

        self.init_ui()

    def init_ui(self):
        self.buton = QtWidgets.QPushButton("Main Window")
        self.table = QtWidgets.QTableWidget(300, 1)
        self.label = QtWidgets.QLabel("Please enter the number of instructors")
        self.table.setHorizontalHeaderLabels(["Instructors"])
        self.dialogs = list()
        self.textbox = QLineEdit(self)
        h_box = QtWidgets.QHBoxLayout()
        h_box2 = QtWidgets.QHBoxLayout()

        h_box2.addWidget(self.label)
        h_box2.addWidget(self.textbox)
        h_box.addWidget(self.buton)
        h_box.addWidget(self.table)
        v_box = QtWidgets.QVBoxLayout()
        v_box.addLayout(h_box)
        v_box.addLayout(h_box2)
        v_box.addStretch()
        self.setLayout(v_box)
        self.setWindowTitle("Instructor Window")
        self.setGeometry(300, 75, 300, 300)
        self.buton.clicked.connect(self.click)
        self.show()

    def click(self):
        file = QtWidgets.QFileDialog.getOpenFileName()

        numberofi = int(self.textbox.text())
        listofins = []
        for i in range(numberofi):
            listofins.append(self.table.item(i, 0).text())

        f = open(file[0], "r")
        data = f.read()
        data = data.replace(",", "")

        data2 = data.split()
        data2 = np.array(data2)
        numberofj = int(len(data2) / numberofi)
        data2 = data2.reshape(numberofi, numberofj)
        v = np.zeros([numberofi, numberofj])

        def findWord(text, word):
            result = 0
            wordd = ""
            for i in range(len(text)):
                for j in range(len(text) - i):
                    wordd += text[i + j].lower()
                    if len(wordd) == len(word):
                        if wordd == word:
                            result = 1
                        wordd = ""
                        break
            return result

        for i in range(numberofi):
            for j in range(numberofj):
                result_possible = findWord(data2[i][j], "possible")
                result_impossible = findWord(data2[i][j], "impossible")
                result_perfect = findWord(data2[i][j], "perfect")
                v[i][j] = result_possible - result_impossible + result_perfect * 2

        dialog = Window(listt=listofins, numberofi=numberofi, v=v, numberofj=numberofj)
        self.dialogs.append(dialog)
        dialog.show()
