import sys
import api
import os
from urllib.request import Request, urlopen
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import *
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
import VideoWindow
import SimpleBuffer
from PIL import Image

dict = {}

class MyWindow(QMainWindow):
	def __init__(self):
		super().__init__()
		self.settings = {'subreddits': []}
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
		self.setGeometry(100,100,720,500)
		self.stacked_layout.setCurrentIndex(1)

	def simple_layout(self,):
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
		self.username.setFixedWidth(200)
		self.password.setFixedWidth(200)
		self.usernameLabel = QLabel("Username : ")
		self.passwordLabel = QLabel("Password : ")
		submit = QPushButton('submit')
		submit.clicked.connect(self.submitlogin)
		submit.setFixedWidth(200)
		submit.setFixedHeight(40)
		login.addWidget(self.usernameLabel)
		login.addWidget(self.username)
		login.addWidget(self.passwordLabel)
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

		self.ImageLabel = QLabel()
		self.VideoWindow = VideoWindow.VideoWindow(self)
		
		self.stacked_media_layout = QStackedLayout()
		self.stacked_media_layout.addWidget(self.VideoWindow)
		self.stacked_media_layout.addWidget(self.ImageLabel)
		
		mediabox = QGroupBox('')
		mediabox.setLayout(self.stacked_media_layout)

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
		self.addSub = QLineEdit()
		addSubButton = QPushButton('Add Sub')
		addSubButton.clicked.connect(self.addSubReddit)
		
		headerContainer = QHBoxLayout()
		headerContainer.addWidget(self.addSub)
		headerContainer.addWidget(addSubButton)
		
		gbox = QGroupBox('')
		gbox.setLayout(headerContainer)
		return gbox

	def sideBar(self):
		subreddits = api.getSubreddits()
		self.subRedditButtons = QVBoxLayout()
		for r in subreddits:
			temp = QPushButton(r['url'][3:-1])
			temp.clicked.connect(self.removeSubReddit)
			self.subRedditButtons.addWidget(temp)

		gbox = QGroupBox()
		gbox.setLayout(self.subRedditButtons)
		return gbox
		
	def footer(self):
		vbox = QVBoxLayout()
		contentlabel = QLabel('this is footer label')
		vbox.addWidget(contentlabel)
		gbox = QGroupBox('')
		gbox.setLayout(vbox)
		return gbox
		
	def addSubReddit(self):
		newsub = self.addSub.text().upper()
		self.settings['subreddits'].append(newsub)
		button = QPushButton(newsub)
		button.clicked.connect(self.removeSubreddit)
		self.subredditbuttons.addWidget(button)

	def changemedia(self):
		if os.path.exists('media\\' + self.posts[self.currindex]['id'] + '.mp4'):
			self.VideoWindow.openFile('media\\' + self.posts[self.currindex]['id'] + '.mp4')
			self.stacked_media_layout.setCurrentIndex(0)
		else:
			hdr = { 'User-Agent' : 'Just a final project' }
			req = Request(self.posts[self.currindex]['url'], headers=hdr)
			data = urlopen(req).read()
			pixmap = QPixmap()
			pixmap.loadFromData(data)
			if (pixmap.isNull()): # this will link to the imgur image rather than the imgurs page
				data = urlopen(self.posts[self.currindex]['url'] + '.jpg').read()
				pixmap.loadFromData(data)
			#fixedPixmap is to change the size of the media, default (1280, 720)
			fixedPixmap = pixmap.scaled(640, 480, Qt.KeepAspectRatio, Qt.FastTransformation)
			self.ImageLabel.setPixmap(fixedPixmap)
			self.stacked_media_layout.setCurrentIndex(1)

	def prevmedia(self):
		if self.currindex > 0:
			self.currindex -= 1
		self.changemedia()

	def nextmedia(self):
		if self.currindex < len(self.posts) - 1:
			self.currindex += 1
		self.changemedia()

	def submitlogin(self):
		self.display_simple_layout()
		self.posts = api.getPosts('VIDEOS', count=10)
		#self.buf = SimpleBuffer.Buffer(self.posts, 'media')
		self.changemedia()
		return

	def removeSubReddit(self):
		self.settings['subreddits'].remove(self.sender().text())
		self.subRedditButtons.removeWidget(self.sender())
		self.sender().deleteLater()

def main():
	app = QApplication(sys.argv)
	win = MyWindow()
	win.show()
	sys.exit(app.exec_())

if __name__ == '__main__':
	main()
