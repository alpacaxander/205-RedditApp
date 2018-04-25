import sys 
#import api
from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import *
from PIL import Image

dict = {}

class MyWindow(QMainWindow):
	def __init__(self):
		super().__init__()
		self.posts = [{'title': '1st'},{'title': '2st'},{'title': '3st'},{'title': '4st'},{'title': '5st'},{'title': '6st'},{'title': '7st'}]
		self.currindex = 0
		self.stacked_layout = QStackedLayout()
		self.stacked_layout.addWidget(self.login())
		self.stacked_layout.addWidget(self.simple_layout())
		self.central_widget = QWidget()
		self.central_widget.setLayout(self.stacked_layout)
		self.setCentralWidget(self.central_widget)
		
	def display_simple_layout(self):
		self.setWindowTitle("Simple Reddit Lauout - Group 10")
		self.setWindowIcon(QIcon("icon.png"))
		self.setGeometry(100,100,700,500)
		self.stacked_layout.setCurrentIndex(1)
	
	def simple_layout(self):
		#Simple Layout is housed in a vertical Layout
		vert = QVBoxLayout()
		#header is a vertical layout that holds the header info
		header = QHBoxLayout()
		#contentBox holds the content and the side bar
		contentBox = QHBoxLayout()
		#footerBox holds the footer
		footerBox = QHBoxLayout()
		#adding widgets to the layouts
		#.addWidget(widget, weight of the layout)
		header.addWidget(self.header())
		contentBox.addWidget(self.sideBar() , 1)
		contentBox.addWidget(self.content() , 5)
		footerBox.addWidget(self.footer())
		#adding the layouts to the main "vert" layout
		#.addLayout(layout , weight of the layout)
		vert.addLayout(header , 1)
		vert.addLayout(contentBox ,14)
		vert.addLayout(footerBox , 1)
		
		simplebox = QGroupBox('')
		simplebox.setLayout(vert)
		return simplebox
		
	def login(self):
		login = QVBoxLayout()
		self.username = QLineEdit()
		self.password = QLineEdit()
		submit = QPushButton('submit')
		submit.clicked.connect(self.submitlogin)
		login.addWidget(self.username)
		login.addWidget(self.password)
		login.addWidget(submit)
		loginbox = QGroupBox('')
		loginbox.setLayout(login)
		return loginbox
		
	def content(self, title='this is title'):
		voting = QVBoxLayout()
		upvote = QPushButton('upvote')
		downvote = QPushButton('downvote')
		voting.addWidget(upvote)
		voting.addWidget(downvote)
		votingbox = QGroupBox('')
		votingbox.setLayout(voting)
		
		vbox = QVBoxLayout()
		prev = QPushButton('prev')
		next = QPushButton('next')
		prev.clicked.connect(self.prevmedia)
		next.clicked.connect(self.nextmedia)
		vbox.addWidget(prev)
		vbox.addWidget(next)
		controlbox = QGroupBox('')
		controlbox.setLayout(vbox)
		
		media = QVBoxLayout()
		self.mediatitle = QLabel(title)
		media.addWidget(self.mediatitle)
		media.addWidget(QLabel('this will be image')) # TODO make function that returns widget with media
		mediabox = QGroupBox('')
		mediabox.setLayout(media)
		
		content = QHBoxLayout()
		content.addWidget(controlbox)
		content.addWidget(votingbox)
		content.addWidget(mediabox)
		self.contentbox = QGroupBox('')
		self.contentbox.setLayout(content)
		
		# add button to open image
		# add button to go to post on reddit
		return self.contentbox

	def header(self):
		vbox = QVBoxLayout()
		contentlabel = QLabel('this is header label')
		vbox.addWidget(contentlabel)
		gbox = QGroupBox('')
		gbox.setLayout(vbox)
		return gbox
	
	def sideBar(self):
		return QGroupBox('SideBar Title')
	def footer(self):
		return QGroupBox('Footer Title')
	@pyqtSlot()
	def changemedia(self):
		self.mediatitle.setText(self.posts[self.currindex]['title'])
		
	def prevmedia(self):
		if self.currindex > 0:
			self.currindex -= 1
		self.changemedia()

	def nextmedia(self):
		if self.currindex < len(self.posts):
			self.currindex += 1
		self.changemedia()
		
	def submitlogin(self):
		self.display_simple_layout()
		#self.posts = api.getFrontPage(count=10)
		return

def main():
	app = QApplication(sys.argv)
	win = MyWindow()
	win.show()
	sys.exit(app.exec_())
	
if __name__ == '__main__':
	main()