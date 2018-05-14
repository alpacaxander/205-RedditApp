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
		self.setGeometry(100,100,1080,900)
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
		self.setWindowIcon(QIcon("icon.png"))
		login = QVBoxLayout()
		usrbox = QHBoxLayout()
		passbox = QHBoxLayout()
		btn = QHBoxLayout()
		space = QHBoxLayout()
		self.setGeometry(100,100,200,100)
		self.username = QLineEdit()
		self.password = QLineEdit()
		self.username.setFixedWidth(200)
		self.password.setFixedWidth(200)
		#LAAAAZY
		self.spaces = QLabel("    ")
		self.cred = QLabel("                                Reddit Desktop Application™")
		self.usernameLabel = QLabel("Username : ")
		self.passwordLabel = QLabel("Password : ")
		self.submit = QPushButton('submit')
		self.submit.clicked.connect(self.submitlogin)
		self.submit.setFixedWidth(200)
		self.submit.setFixedHeight(40)
		# login.addWidget(self.usernameLabel)
		# login.addWidget(self.username)
		# login.addWidget(self.passwordLabel)
		# login.addWidget(self.password)
		# login.addWidget(submit)
		usrbox.addWidget(self.usernameLabel)
		usrbox.addWidget(self.username)

		space.addWidget(self.cred)

		passbox.addWidget(self.passwordLabel)
		passbox.addWidget(self.password)
		btn.addWidget(self.spaces)
		btn.addWidget(self.submit)
		btn.addWidget(self.spaces)
		login.addLayout(usrbox)
		login.addLayout(passbox)
		login.addLayout(btn)
		login.addLayout(space)
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
		#content.addWidget(controlbox)
		# content.addWidget(votingbox)
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
		self.scroll = QScrollArea(self)
		self.scroll.setWidgetResizable(True)
		self.scroll.setFixedWidth(180)
		self.subRedditButtons.addWidget(self.scroll)
		scrollContent = QWidget(self.scroll)
		self.scrollLayout = QVBoxLayout(scrollContent)
		scrollContent.setLayout(self.scrollLayout)
		for r in subreddits:
			temp = QPushButton(r['url'][3:-1])
			self.settings['subreddits'].append(r['url'][3:-1])
			temp.clicked.connect(self.removeSubReddit)
			self.scrollLayout.addWidget(temp)
		self.scroll.setWidget(scrollContent)
		#gbox = QGroupBox()
		# gbox.setLayout(self.scroll)
		return self.scroll

	def footer(self):
		hbox = QHBoxLayout()
		prev = QPushButton('prev')
		next = QPushButton('next')
		prev.clicked.connect(self.prevmedia)
		next.clicked.connect(self.nextmedia)
		#I know, im lazy
		contentlabel = QLabel('                                                 ')
		hbox.addWidget(contentlabel)
		hbox.addWidget(prev)
		hbox.addWidget(next)
		gbox = QGroupBox('')
		gbox.setLayout(hbox)
		return gbox

	def addSubReddit(self):
		newsub = self.addSub.text().upper()
		self.settings['subreddits'].append(newsub)
		button = QPushButton(newsub)
		button.clicked.connect(self.removeSubReddit)
		# self.subRedditButtons.addWidget(button)
		self.scrollLayout.addWidget(button)

	def changemedia(self):
		print(self.posts[self.currindex]['url'])
		dir = os.path.join(os.path.curdir, 'media', self.posts[self.currindex]['id'] + '.mp4')
		if os.path.exists(dir):
			self.VideoWindow.openFile(dir)
			self.stacked_media_layout.setCurrentIndex(0)
		else:
			hdr = { 'User-Agent' : 'Just a final project' }
			req = Request(self.posts[self.currindex]['url'], headers=hdr)
			data = urlopen(req).read()
			pixmap = QPixmap()
			pixmap.loadFromData(data)
			#if (pixmap.isNull()): # this will link to the imgur image rather than the imgurs page
			#	data = urlopen(Request(self.posts[self.currindex]['url'] + '.jpg', headers=hdr)).read()
			#	pixmap.loadFromData(data)
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
		print(self.settings)
		self.display_simple_layout()
		self.posts = []
		self.posts = api.getPosts('GIFS', count=20)
		#for i in self.settings['subreddits']:
		#	self.posts.extend(api.getPosts(i, count=2))
		self.buf = SimpleBuffer.Buffer(self.posts, 'media')
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
