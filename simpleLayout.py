#GROUP 10
#!/usr/bin/env python
'''
Course: CST205-01
Title: RedditApp (final project)
Abstract: A desktop app that can browse reddit
Authors: Kyle Hays, Alexander Paulsell, Anthony Zerka, Brett stevenson
Date: 14 may 2018
'''
#Athors: Anthony Zerka
#Abstract: Organization of window layout
import sys
from PyQt5 import QtWidgets , QtGui , QtCore
from PyQt5.QtWidgets import *
import PyQt5.QtCore
from PyQt5.QtCore import *

class MyWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        #Set basic window Attributes :
        self.setWindowTitle("Simple Reddit Lauout - Group 10")
        #added window icon (subject to change)
        self.setWindowIcon(QtGui.QIcon("icon.png"))
        self.setGeometry(100,100,700,500)
        #Simple Layout is housed in a vertical Layout
        vert = QtWidgets.QVBoxLayout()
        #header is a vertical layout that holds the header info
        header = QtWidgets.QHBoxLayout()
        #contentBox holds the content and the side bar
        contentBox = QtWidgets.QHBoxLayout()
        #footerBox holds the footer
        footerBox = QtWidgets.QHBoxLayout()
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
        self.setLayout(vert)
        #show window
        self.show()
        sys.exit(app.exec_())
    #METHODS FOR TESTING :
    def content(self):
        return QtWidgets.QGroupBox('Content Window Title')
    def header(self):
        return QtWidgets.QGroupBox('Header Title')
    def sideBar(self):
        return QtWidgets.QGroupBox('SideBar Title')
    def footer(self):
        return QtWidgets.QGroupBox('Footer Title')
#Event Loop
app = QtWidgets.QApplication(sys.argv)
win = MyWindow()
