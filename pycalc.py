from PyQt5.QtCore import QUrl, pyqtSlot
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtGui import *
import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QPushButton, QAction, QLineEdit, QMessageBox


class Calculator(QWidget):

	def __init__(self, name):
		super().__init__()
		self.title = "PyCalc"
		self.name = name
		self.initUI()
		

	def initUI(self):
		self.setWindowTitle(self.title)

		self.label = QLabel('', self)

		self.calcButton = QPushButton('Calculate!', self)
		self.calcButton.clicked.connect(self.calculate)

		self.textbox = QLineEdit(self)
		self.textbox.setPlaceholderText("Hello " + self.name + ". Please enter a problem")
		self.textbox.returnPressed.connect(self.calculate)

		self.layout = QVBoxLayout(self)
		self.layout.addWidget(self.label)
		self.layout.addWidget(self.textbox)
		self.layout.addWidget(self.calcButton)

		self.show()
		
	def calculate(self):
		stuff = self.textbox.text().split(" ")
		if stuff[1] == '+':
			self.label.setText(str(int(stuff[0]) + int(stuff[2])))
		if stuff[1] == '-':
			self.label.setText(str(int(stuff[0]) - int(stuff[2])))
		if stuff[1] == '/':
			self.label.setText(str(int(stuff[0]) / int(stuff[2])))
		if stuff[1] == '*':
			self.label.setText(str(int(stuff[0]) * int(stuff[2])))
		self.textbox.setText('')




