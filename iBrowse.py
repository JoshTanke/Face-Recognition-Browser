from PyQt5.QtCore import QUrl, pyqtSlot
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtGui import *
import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QPushButton, QAction, QLineEdit, QMessageBox
import face_recognize
import create_database
import _thread
import pycalc



class DevBox(QWidget):

	def __init__(self, webWindow):
		super().__init__()

		self.ww = webWindow

		self.label = QLabel('', self)

		self.textbox = QLineEdit(self)
		self.textbox.setPlaceholderText("Enter a command.  Type 'help' for options.")
		self.textbox.returnPressed.connect(self.devGo)

		self.layout = QVBoxLayout(self)
		self.layout.addWidget(self.label)
		self.layout.addWidget(self.textbox)

		self.show()

	def devGo(self):
		self.label.setText('')

		if self.textbox.text() == 'help':
			self.textbox.setText('')
			self.label.setText('Commands: addSite, addUser(name)')

		elif self.textbox.text() == 'addSite':
			self.textbox.setText('')
			self.ww.addSite()

		elif self.textbox.text()[0:7] == 'addUser':

			name = self.textbox.text()[8:-1]
			_thread.start_new_thread(face_recognize.addUser, (name, ))
			self.ww.name = name
			self.ww.homeScreen()

		elif self.textbox.text() == 'pyCalc':
			_thread.start_new_thread(pycalc.openCalc, (self.ww.name, ))


class SearchBar(QWidget):

	def __init__(self, webWindow):
		super().__init__()

		self.ww = webWindow

		self.textbox = QLineEdit(self)
		self.textbox.setPlaceholderText("Enter a url")
		self.textbox.returnPressed.connect(self.searchButton)
		
		self.homeButton = QPushButton('Home', self)
		self.homeButton.clicked.connect(self.goHome)

		iconOne = QIcon()
		iconOne.addPixmap(QPixmap("left-arrow.ico"))
		iconTwo = QIcon()
		iconTwo.addPixmap(QPixmap("right-arrow.ico"))

		self.backButton = QPushButton()
		self.backButton.setIcon(iconOne)
		self.backButton.clicked.connect(self.goBack)
		self.forwardButton = QPushButton()
		self.forwardButton.setIcon(iconTwo)
		self.forwardButton.clicked.connect(self.goForward)

		self.layout = QHBoxLayout(self)
		self.layout.addWidget(self.backButton)
		self.layout.addWidget(self.forwardButton)
		self.layout.addWidget(self.textbox)
		self.layout.addWidget(self.homeButton)

		self.show()

	def searchButton(self):
		url = self.textbox.text()
		self.ww.changeUrl('https://www.' + url)

	def goHome(self):
		self.textbox.setText("")
		self.ww.homeScreen()

	def goBack(self):
		self.ww.changeUrl(self.ww.previousUrl)
		#self.textbox.setText(self.ww.previousUrl)
		print(self.ww.previousUrl)

	def goForward(self):
		self.ww.changeUrl(self.ww.nextUrl)
		#self.textbox.setText(self.ww.nextUrl)
		print(self.ww.nextUrl)


class WebWindow(QWebEngineView):

	def __init__(self, name):
		super().__init__()
		
		self.name = name
		self.websites = [['https://www.youtube.com/', 'YouTube'], 
			['https://www.google.com/', 'Google'], ['https://www.facebook.com/', 'Facebook']]
		self.nextUrl = None
		self.previousUrl = None
		self.homeScreen()

	def changeUrl(self, url):
		if self.previousUrl != url:
			self.nextUrl = url
	
		self.previousUrl = self.currentUrl
		self.currentUrl = url
		self.setUrl(QUrl(self.currentUrl))

	def homeScreen(self):
		if self.name == None:
			self.name = "Guest</h1><h1>Type 'addUser' to create an account."

		self.currentUrl = None
		html = """
        	<html>
        	<style type="text/css">
            	h1 {color: black;
            		text-align: center;
            	}
            	div {color: blue;
            		text-align: center;
            	}
        	</style>
        	<body>   
        	<h1>Hello """ + self.name + """
        	</h1>
        	<div>Welcome to iBrowse</div>
        	</body>   
        	</html>
    		"""
		
		for i in range(len(self.websites)):
			html += """<img width="50" height="50" src="https://www.""" + self.websites[i][1] + """.com/favicon.ico"><a href=" """ + self.websites[i][0] + """">""" + self.websites[i][1] + """</a></img><br>"""

		self.setHtml(html)

	def addSite(self):
		if self.currentUrl != None:
			parts = self.currentUrl.split('.')
			siteInfo = [self.currentUrl, parts[1]]
			if siteInfo not in self.websites:
				self.websites.append(siteInfo)	

		

class MainWindow(QWidget):

	def __init__(self, name):
		super().__init__()
		self.title = 'iBrowse'
		self.name = name
		self.initUI()
		
	def initUI(self):
		self.setWindowTitle(self.title)

		self.ww = WebWindow(self.name)
		self.searchBar = SearchBar(self.ww)
		self.devBox = DevBox(self.ww)

		self.layout = QVBoxLayout(self)
		self.layout.addWidget(self.searchBar)
		self.layout.addWidget(self.ww)
		self.layout.addWidget(self.devBox)

		self.show()


def main():
	
	
	name = face_recognize.checkFace()

	if name != None:
		name = name.title()

	app = QApplication(sys.argv)
	main = MainWindow(name)
	app.exec()

if __name__ == "__main__":
	main()

