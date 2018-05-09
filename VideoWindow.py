#!/usr/bin/env python

from PyQt5.QtCore import *
from PyQt5.QtMultimedia import *
from PyQt5.QtMultimediaWidgets import *
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import sys
 
class VideoWindow(QMainWindow):

	def __init__(self, parent=None):
		super(VideoWindow, self).__init__(parent)
		
		self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)

		videoWidget = QVideoWidget()

		self.playButton = QPushButton()
		self.playButton.setEnabled(False)
		self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
		self.playButton.clicked.connect(self.play)

		self.positionSlider = QSlider(Qt.Horizontal)
		self.positionSlider.setRange(0, 0)
		self.positionSlider.sliderMoved.connect(self.setPosition)

		wid = QWidget(self)
		self.setCentralWidget(wid)

		controlLayout = QHBoxLayout()
		controlLayout.setContentsMargins(0, 0, 0, 0)
		controlLayout.addWidget(self.playButton)
		controlLayout.addWidget(self.positionSlider)

		layout = QVBoxLayout()
		layout.addWidget(videoWidget)
		layout.addLayout(controlLayout)

		wid.setLayout(layout)

		self.mediaPlayer.setVideoOutput(videoWidget)
		self.mediaPlayer.stateChanged.connect(self.mediaStateChanged)
		self.mediaPlayer.positionChanged.connect(self.positionChanged)
		self.mediaPlayer.durationChanged.connect(self.durationChanged)

	def openFile(self, fileName):
		self.mediaPlayer.setMedia(
				QMediaContent(QUrl.fromLocalFile(fileName)))
		self.playButton.setEnabled(True)

	def play(self):
		if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
			self.mediaPlayer.pause()
		else:
			self.mediaPlayer.play()
 
	def mediaStateChanged(self, state):
		if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
			self.playButton.setIcon(
					self.style().standardIcon(QStyle.SP_MediaPause))
		else:
			self.playButton.setIcon(
					self.style().standardIcon(QStyle.SP_MediaPlay))

	def positionChanged(self, position):
		self.positionSlider.setValue(position)

	def durationChanged(self, duration):
		self.positionSlider.setRange(0, duration)

	def setPosition(self, position):
		self.mediaPlayer.setPosition(position)