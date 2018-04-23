import sys 
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QComboBox, QHBoxLayout, QGroupBox, QLineEdit
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QPixmap
from PIL import Image

dict = {}

class MyWindow(QWidget):
	def __init__(self):
		super().__init__()
		self.posts = [{'title': '1st'},{'title': '2st'},{'title': '3st'},{'title': '4st'},{'title': '5st'},{'title': '6st'},{'title': '7st'}]
		self.currindex = 0
		mbox = QVBoxLayout()
		mbox.addWidget(self.login())
		self.setLayout(mbox)
		
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
	
	def successfullogin(self):
		return
		
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
		return

def main():
	app = QApplication(sys.argv)
	win = MyWindow()
	win.show()
	sys.exit(app.exec_())
	
if __name__ == '__main__':
	main()