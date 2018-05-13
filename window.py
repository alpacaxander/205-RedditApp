#!/usr/bin/env python

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
		self.setGeometry(100,100,720,500)
		self.stacked_layout.setCurrentIndex(1)

	def simple_layout(self,):
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
		content.addWidget(controlbox)
		content.addWidget(votingbox)
		content.addWidget(mediabox)
		self.contentbox = QGroupBox('')
		self.contentbox.setLayout(content)
		
		return self.contentbox

	def header(self):
		self.addSubText = QLineEdit()#input new sub to be added to next refreshContent
		addSubButton = QPushButton('Add Sub')
		addSubButton.clicked.connect(self.addSubReddit)
		
		headerContainer = QHBoxLayout()
		headerContainer.addWidget(self.addSubText)
		headerContainer.addWidget(addSubButton)
		
		gbox = QGroupBox('')
		gbox.setLayout(headerContainer)
		return gbox

	def sideBar(self):
		subreddits = ['PICS', 'GIFS', 'VIDEOS', 'WORLDNEWS']#default subs
		self.subRedditButtons = QVBoxLayout()
		self.spinBox = QSpinBox()
		self.spinBox.setValue(5)#how many posts to get from each sub
		self.subRedditButtons.addWidget(self.spinBox)
		for r in subreddits:
			temp = QPushButton(r)
			self.settings['subreddits'].append(r.upper())
			temp.clicked.connect(self.removeSubReddit)
			self.subRedditButtons.addWidget(temp)

		gbox = QGroupBox()
		gbox.setLayout(self.subRedditButtons)
		return gbox
		
	def footer(self):
		vbox = QVBoxLayout()
		contentlabel = QLabel()
		vbox.addWidget(contentlabel)
		linkButton = QPushButton('See post url')#go to post url in default web browser
		linkButton.clicked.connect(self.hyperlink)
		vbox.addWidget(linkButton)
		refreshButton = QPushButton('Refresh Content')#search for posts with new perameters
		refreshButton.clicked.connect(self.refreshContent)
		vbox.addWidget(refreshButton)
		gbox = QGroupBox('')
		gbox.setLayout(vbox)
		
		return gbox
		
	def addSubReddit(self):#handle user adding new subreddits
		newsub = self.addSubText.text().upper()
		self.settings['subreddits'].append(newsub)
		button = QPushButton(newsub)
		button.clicked.connect(self.removeSubReddit)
		self.subRedditButtons.addWidget(button)

	def changemedia(self):#handle displaying new post
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
