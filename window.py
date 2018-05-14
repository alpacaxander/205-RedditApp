#!/usr/bin/env python
'''
Course: CST205-01
Title: RedditApp (final project)
Abstract: A desktop app that can browse reddit
Authors: Kyle Hays, Alexander Paulsell, Anthony Zerka, Brett stevenson
Date: 14 may 2018
https://github.com/tterb/205-RedditApp/tree/saftyBranch
'''
#Athors: Alexander Paulsell (Functionality), Anthony Zerka (Organization)
#Abstract: Uses api / buffer to display reddit content
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
import webbrowser
from PIL import Image

dict = {}

class MyWindow(QMainWindow):
	def __init__(self):#set up login and simple_layout, show login, then after login show simple_layout
		super().__init__()
		self.settings = {'subreddits': []}
		self.currindex = 0
		self.stacked_layout = QStackedLayout()
		self.stacked_layout.addWidget(self.login())
		self.stacked_layout.addWidget(self.simple_layout())
		self.central_widget = QWidget()
		self.central_widget.setLayout(self.stacked_layout)
		self.setCentralWidget(self.central_widget)

	def display_simple_layout(self):#resize to prepare for switch to simple_layout
		self.setWindowTitle("Simple Reddit Lauout - Group 10")
		self.setWindowIcon(QIcon("icon.png"))
		self.setGeometry(100,100,1080,900)
		self.stacked_layout.setCurrentIndex(1)

	def simple_layout(self,):
		#Simple Layout is housed in a vertical Layout
		vert = QVBoxLayout()
		header = QHBoxLayout()
		contentBox = QHBoxLayout()
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

	def login(self):#take in username and password to access reddit api
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

	def content(self):#where the content is displayed
		voting = QVBoxLayout()
		upvote = QPushButton('upvote')
		downvote = QPushButton('downvote')
		voting.addWidget(upvote)
		voting.addWidget(downvote)
		votingbox = QGroupBox('')
		votingbox.setLayout(voting)

		vbox = QVBoxLayout()
		prev = QPushButton('prev')#change to next/prev post
		next = QPushButton('next')
		prev.clicked.connect(self.prevmedia)
		next.clicked.connect(self.nextmedia)
		vbox.addWidget(prev)
		vbox.addWidget(next)
		controlbox = QGroupBox('')
		controlbox.setLayout(vbox)

		self.title = QLabel()#to display title of post		
		self.ImageLabel = QLabel()#to display images and text posts
		self.VideoWindow = VideoWindow.VideoWindow(self)#to display videos/gifs
		
		self.stacked_media_layout = QStackedLayout()#switch between display methods
		self.stacked_media_layout.addWidget(self.VideoWindow)
		self.stacked_media_layout.addWidget(self.ImageLabel)
		
		mediaBox = QGroupBox('')
		mediaBox.setLayout(self.stacked_media_layout)
		
		contentVbox = QVBoxLayout()
		contentVbox.addWidget(self.title)
		contentVbox.addWidget(mediaBox)
		
		mediabox = QGroupBox('')
		mediabox.setLayout(contentVbox)

		content = QHBoxLayout()
		#content.addWidget(controlbox)
		# content.addWidget(votingbox)
		content.addWidget(mediabox)
		self.contentbox = QGroupBox('')
		self.contentbox.setLayout(content)
		
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
		subreddits = ['PICS', 'GIFS', 'VIDEOS', 'WORLDNEWS']#default subs
		self.subRedditButtons = QVBoxLayout()
		self.spinBox = QSpinBox()
		self.spinBox.setValue(5)#how many posts to get from each sub
		
		self.scroll = QScrollArea(self)
		self.scroll.setWidgetResizable(True)
		self.scroll.setFixedWidth(180)
		self.subRedditButtons.addWidget(self.scroll)
		scrollContent = QWidget(self.scroll)
		self.scrollLayout = QVBoxLayout(scrollContent)
		scrollContent.setLayout(self.scrollLayout)
		self.scrollLayout.addWidget(self.spinBox)
		for r in subreddits:
			temp = QPushButton(r)
			self.settings['subreddits'].append(r.upper())
			temp.clicked.connect(self.removeSubReddit)
			self.scrollLayout.addWidget(temp)
		self.scroll.setWidget(scrollContent)
		return self.scroll

	def footer(self):
		hbox = QHBoxLayout()
		prev = QPushButton('prev')
		next = QPushButton('next')
		refreshButton = QPushButton('Refresh Content')#search for posts with new perameters
		linkButton = QPushButton('See post url')#go to post url in default web browser
		prev.clicked.connect(self.prevmedia)
		next.clicked.connect(self.nextmedia)
		linkButton.clicked.connect(self.hyperlink)
		refreshButton.clicked.connect(self.refreshContent)
		contentlabel = QLabel('                                                 ')
		hbox.addWidget(contentlabel)
		hbox.addWidget(prev)
		hbox.addWidget(next)
		hbox.addWidget(refreshButton)
		hbox.addWidget(linkButton)
		gbox = QGroupBox('')
		gbox.setLayout(hbox)
		return gbox

	def addSubReddit(self):
		newsub = self.addSub.text().upper()
		self.settings['subreddits'].append(newsub)
		button = QPushButton(newsub)
		button.clicked.connect(self.removeSubReddit)
		self.scrollLayout.addWidget(button)

	def changemedia(self):
		print(self.posts[self.currindex]['url'])
		self.title.setText(self.posts[self.currindex]['title'])
		dir = os.path.join(os.path.curdir, 'media', self.posts[self.currindex]['id'] + '.mp4')
		if self.posts[self.currindex]['is_self'] :
			self.stacked_media_layout.setCurrentIndex(1)
			self.ImageLabel.setText(self.posts[self.currindex]['selftext'])
		elif os.path.exists(dir):
			self.VideoWindow.openFile(dir)
			self.VideoWindow.play()
			self.stacked_media_layout.setCurrentIndex(0)
		else:
			hdr = { 'User-Agent' : 'Just a final project' }
			req = Request(self.posts[self.currindex]['url'], headers=hdr)
			data = urlopen(req).read()
			pixmap = QPixmap()
			pixmap.loadFromData(data)
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

	def hyperlink(self):
		webbrowser.open(self.posts[self.currindex]['url'])
	
	def submitlogin(self):
		self.display_simple_layout()
		self.refreshContent()
		return
		
	def refreshContent(self):
		self.currindex = 0
		self.posts = []
		for i in self.settings['subreddits']:
			self.posts.extend(api.getPosts(i, count=self.spinBox.value()))
		self.buf = SimpleBuffer.Buffer(self.posts, 'media')
		self.changemedia()

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
