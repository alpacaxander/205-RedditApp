import sys
import api
from urllib.request import Request, urlopen
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import *
from PIL import Image

dict = {}

class MyWindow(QMainWindow):
	def __init__(self):
		super().__init__()
		self.settings = {'subreddits': ['PICS', 'GIFS', 'VIDEOS']}

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
		self.setGeometry(100,100,1000,720)
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
		scroll = QScrollArea()
		scroll.setWidgetResizable(True)
		scroll.setFixedHeight(60)
		scroll.setWidget(self.header())
		header.addWidget(scroll)
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
		#The login screen is fixed to this width/height
		#self.setFixedWidth(230)
		#self.setFixedHeight(200)
		#self.setGeometry(100,100,230,200)
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

		vmedia = QVBoxLayout()
		self.mediatitle = QLabel(title)
		self.mediatitle.setWordWrap(True)#Set label to word wrap, so it doesnt mess up the size of the layout (and for aesthetic reasons)
		self.media = QLabel('this will be image')



		vmedia.addWidget(self.mediatitle)
		vmedia.addWidget(self.media) # TODO make function that returns widget with media
		mediabox = QGroupBox('')
		mediabox.setLayout(vmedia)

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
		subreddits = api.getSubreddits()
		self.subredditbuttons = QHBoxLayout()
		for r in subreddits:
			temp = QPushButton(r['title'])
			temp.clicked.connect(self.setsubreddit)
			self.subredditbuttons.addWidget(temp)

		gbox = QGroupBox('')
		gbox.setLayout(self.subredditbuttons)
		return gbox

	def sideBar(self):
		self.inputsubreddit = QLineEdit()
		self.inputsubreddit.setFixedWidth(200)
		add = QPushButton('Add Subreddit')
		add.clicked.connect(self.addsubreddit)
		vbox = QVBoxLayout()
		vbox.addWidget(self.inputsubreddit)
		vbox.addWidget(add)
		gbox = QGroupBox()
		gbox.setLayout(vbox)
		return gbox

	def footer(self):
		vbox = QVBoxLayout()
		contentlabel = QLabel('this is footer label')
		vbox.addWidget(contentlabel)
		gbox = QGroupBox('')
		gbox.setLayout(vbox)
		return gbox
	@pyqtSlot()
	def addsubreddit(self):
		newsub = self.inputsubreddit.text().upper()
		self.settings['subreddits'].append(newsub)
		button = QPushButton('-' + newsub)
		button.clicked.connect(self.setsubreddit)
		self.subredditbuttons.addWidget(button)

	def changemedia(self):
		print(self.posts[self.currindex]['url'])
		self.mediatitle.setText(self.posts[self.currindex]['title'])
		'''
		urllib.request.urlretrieve(self.posts[self.currindex]['url'].read(), 'temp.gif')

		movie = QMovie('temp.gif', QByteArray(), self)
		movie.setCacheMode(QMovie.CacheAll)
		movie.setSpeed(100)
		self.media.setMovie(movie)
		movie.start()
		movie.loopCount()

		'''
		hdr = { 'User-Agent' : 'Just a final project' }
		req = Request(self.posts[self.currindex]['url'], headers=hdr)
		data = urlopen(req).read()
		pixmap = QPixmap()
		pixmap.loadFromData(data)
		#if (pixmap.isNull()): # this will link to the imgur image rather than the imgurs page
		#	data = urlopen(self.posts[self.currindex]['url'] + '.jpg').read()
		#	pixmap.loadFromData(data)
		#fixedPixmap is to change the size of the media, default (1280, 720)
		fixedPixmap = pixmap.scaled(640, 480, Qt.KeepAspectRatio, Qt.FastTransformation)
		self.media.setPixmap(fixedPixmap)


	def prevmedia(self):
		if self.currindex > 0:
			self.currindex -= 1
		self.changemedia()

	def nextmedia(self):
		if self.currindex < len(self.posts) - 1:
			self.currindex += 1
		self.changemedia()

	def submitlogin(self):
		#The screen is fixed to this width/height
		#self.setFixedWidth(720)
		#self.setFixedHeight(600)

		self.display_simple_layout()
		self.posts = api.getPosts('GIFS', count=10)
		self.changemedia()
		return

	def setsubreddit(self):
		if self.sender().text()[0] == '-' :
			self.settings['subreddits'].remove(self.sender().text()[1:])
			self.sender().setText(self.sender().text()[1:])
		else:
			self.settings['subreddits'].append(self.sender().text())
			self.sender().setText('-' + self.sender().text())


def main():
	app = QApplication(sys.argv)
	win = MyWindow()
	win.show()
	sys.exit(app.exec_())

if __name__ == '__main__':
	main()
