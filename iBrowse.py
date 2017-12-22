from PyQt5.QtCore import QUrl, pyqtSlot
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtGui import *
import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QPushButton, QAction, QLineEdit, QMessageBox
import face_recognize
import create_database
import _thread
import speech_recognition as sr
import database
from linkedlist import *

#this class defines the command line at the bottom of the application.
class DevBox(QWidget):

	#initalizes the layout
	def __init__(self, webWindow):
		super().__init__()

		self.ww = webWindow

		self.label = QLabel('', self)

		self.textbox = QLineEdit(self)
		self.textbox.setPlaceholderText("Enter a command.  Type 'help' for options.")
		self.textbox.returnPressed.connect(self.devGo)

		self.voiceButton = QPushButton('Audio', self)
		self.voiceButton.clicked.connect(self.voiceCommand)

		self.layout = QVBoxLayout(self)
		self.layout.addWidget(self.label)
		self.layout.addWidget(self.textbox)
		self.layout.addWidget(self.voiceButton)

		self.show()

	#Defines the logic behind the different commands
	def devGo(self):

		#this boolean is used to restrict guests from using certain features
		cantUse = False
		if self.ww.name == None:
			cantUse = True

		self.label.setText('')

		#lists the different commands
		if self.textbox.text() == 'help':
			self.textbox.setText('')
			self.label.setText('Commands: addSite, addUser(name), clearData, deleteUser, clear')

		#Adds site to the current user's list of sites
		elif self.textbox.text() == 'addSite':
			if cantUse:
				self.textbox.setText('')
				self.label.setText('You must be logged in to use this function.')
				return
			self.textbox.setText('')
			self.ww.addSite()

		#clears user preferences 
		elif self.textbox.text() == 'clearData':
			if cantUse:
				self.textbox.setText('')
				self.label.setText('You must be logged in to use this function.')
				return
			self.textbox.setText('')
			database.deleteUser(self.ww.name)
			database.addUser(self.ww.name)
			self.ww.websites = ['google https://www.google.com/']
			self.ww.websitesDictionary = {'google': 'https://www.google.com/'}
			self.ww.homeScreen()

		#adds a new user to the database and takes images to use for recognition
		elif self.textbox.text()[0:7] == 'addUser':
			name = self.textbox.text()[8:-1]
			_thread.start_new_thread(face_recognize.addUser, (name, ))
			self.ww.name = name.title()
			database.addUser(name.title())
			self.textbox.setText('')
			self.ww.homeScreen()

		#removes user from image database and websites database
		elif self.textbox.text() == 'deleteUser':
			if cantUse:
				self.textbox.setText('')
				self.label.setText('You must be logged in to use this function.')
				return
			self.textbox.setText('')
			database.deleteUser(self.ww.name)
			self.ww.websites = ['google https://www.google.com/']
			self.ww.websitesDictionary = {'google': 'https://www.google.com/'}
			create_database.deleteUser(self.ww.name)
			self.ww.name = None
			self.ww.homeScreen()

		#tool used for debuggin in development
		elif self.textbox.text()[0:15] == 'deleteUserAdmin':
			tempName = self.textbox.text()[16:-1]
			database.deleteUser(tempName)
			create_database.deleteUser(tempName)
			self.ww.homeScreen()

		#clears the label
		elif self.textbox.text() == 'clear':
			self.textbox.setText('')
			self.label.setText('')

		#TODO connect 'Tweet Locate' app
		#elif self.textbox.text() == 'tweetLocate':
			

	#deals with voice commands
	def voiceCommand(self):
		#restricts guests from using this function
		if self.ww.name == None:
			self.label.setText('You must be logged in to use this function.')
			return

		self.label.setText('Please say a command.')

		#turns on microphone and returns audio as a string
		self.r = sr.Recognizer()
		with sr.Microphone() as source:
			audio = self.r.listen(source)

		#defines the logic for each type of voice command
		if 'go to' in self.r.recognize_google(audio):
			self.textbox.setText('')
			items = self.r.recognize_google(audio).split()
			self.goto(items[2].lower())
		elif 'clear data' in self.r.recognize_google(audio):
			self.textbox.setText('')
			database.deleteUser(self.ww.name)
			database.addUser(self.ww.name)
			self.ww.websites = ['google https://www.google.com/']
			self.ww.websitesDictionary = {'google': 'https://www.google.com/'}
			self.ww.homeScreen()
		elif 'add site' in self.r.recognize_google(audio):
			self.textbox.setText('')
			self.ww.addSite()
			self.label.setText('Done')
		elif 'go home' in self.r.recognize_google(audio):
			self.ww.homeScreen()
			self.label.setText('')

	#allows user to change current site with voice command
	def goto(self, address):
		if address in self.ww.websitesDictionary:
			self.ww.changeUrl(self.ww.websitesDictionary[address], True)
		elif address == 'home':
			self.ww.homeScreen()
		else:
			self.label.setText("I don't recognize that website.")


#this class defines the search bar at the top of the application.
class SearchBar(QWidget):

	#class initialization
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

	#changes the url to the user input
	def searchButton(self):
		url = self.textbox.text()
		self.ww.changeUrl('https://www.' + url, True)

	#returns to the home screen defined in the WebWindow class
	def goHome(self):
		self.textbox.setText("")
		self.ww.homeScreen()

	#returns to the previous site
	def goBack(self):
		if self.ww.currentUrl.prev != None:
			self.ww.currentUrl = self.ww.currentUrl.prev
			self.ww.changeUrl(self.ww.currentUrl, False)

	#returns to the next site, if applicable
	def goForward(self):
		if self.ww.currentUrl.next != None:
			self.ww.currentUrl = self.ww.currentUrl.next
			self.ww.changeUrl(self.ww.currentUrl, False)


#this class defines the main web window that hosts the webpage
class WebWindow(QWebEngineView):

	#class intialization
	def __init__(self, name):
		super().__init__()

		self.name = name

		#creates a linked list of websites to be utilized by the forward and backword buttons
		self.urls = DoubleList()

		#retrieves websites for the current user; creates list with only google if user is not found.
		self.websites = database.getUserData(self.name)
		if self.name != None:
			self.websites = list(self.websites[0][1:5])
		else:
			self.websites = ['google https://www.google.com/']

		self.websitesDictionary = {}

		#creates a dictionary of the user websites to increase search time in functions that utilize the list of websites
		for item in self.websites:
			if len(item) > 1:
				data = item.split()
				self.websitesDictionary[data[0]] = data[1]

		self.currentUrl = self.urls.append('home')
		self.homeScreen()

	#changes the url hosted by the QUrl class
	def changeUrl(self, url, new):
		if new:
			self.currentUrl = self.urls.append(url)

		if self.currentUrl.data == 'home':
			self.homeScreen()
			return

		self.setUrl(QUrl(self.currentUrl.data))

	#creates a custom home screen based on what user (or guest) is currently logged in
	def homeScreen(self):
		self.header = self.name
		if self.header == None:
			self.header = "Guest</h1><h1>Type 'addUser' to create an account."

		if self.currentUrl.data != 'home':
			self.currentUrl = self.urls.append('home')

		#welcomes the user
		html = """
        	<html>
        	<style type="text/css">
            	div {
            		color: black;
            		text-align: center;
            	}
            	.myelement{
            		padding-right: 50px;
            	}
        	</style>
        	<body>   
        	<div>
        	<img src="https://image.ibb.co/e74q7m/logo.png" alt="logo" border="0">
        	<h1>Hello """ + self.header + """</h1>
        	</div>
        	</body>   
        	</html>
    		"""
    	#displays the user's websites
		i = 1
		html += "<div>"
		for item in self.websites:
			if len(item) > 0:
				parts = item.split()
				html += """<img width="50" height="50" src="https://www.""" + parts[0] + """.com/favicon.ico"><a class="myelement" href=" """ + parts[1] + """">""" + parts[0].title() + """</a></img>"""
				if i % 2 == 0:
					html += "</div><br><br><div>"
				i += 1

		self.setHtml(html)

	#adds site to users homescreen and includes it in the user's database profile
	def addSite(self):
		if self.currentUrl != None:
			parts = self.currentUrl.data.split('.')
			siteInfo = parts[1] + ' ' + self.currentUrl.data
			if siteInfo not in self.websites:
				database.updateUser(self.name, siteInfo)
				self.websites.append(siteInfo)	
				self.websitesDictionary[parts[1]] = self.currentUrl.data

		
#defines the layout of the application
class MainWindow(QWidget):

	def __init__(self, name):
		super().__init__()
		self.title = 'iBrowse'
		self.name = name
		self.initUI()
	
	#resizes the screen based on the user's monitor size
	def initUI(self):
		self.resize(1200, 1000)
		qr = self.frameGeometry()
		cp = QDesktopWidget().availableGeometry().center()
		qr.moveCenter(cp)
		self.move(qr.topLeft())
		
		self.setWindowTitle(self.title)

		self.ww = WebWindow(self.name)
		self.searchBar = SearchBar(self.ww)
		self.devBox = DevBox(self.ww)

		self.layout = QVBoxLayout(self)
		self.layout.addWidget(self.searchBar)
		self.layout.addWidget(self.ww)
		self.layout.addWidget(self.devBox)

		self.show()

#starts the application
def main():

	name = face_recognize.checkFace()
	app = QApplication(sys.argv)
	main = MainWindow(name)
	app.exec()

	

if __name__ == "__main__":
	main()

