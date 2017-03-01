#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
ZetCode PyQt5 tutorial 

In this example, we select a file with a
QFileDialog and
shows the image in matplotlib (to get coords)

author: Jan Bodnar
website: zetcode.com 
last edited: January 2015
"""

import sys
from PyQt5.QtWidgets import (QMainWindow, QTextEdit, 
    QAction, QFileDialog, QApplication)
from PyQt5.QtGui import QIcon
import numpy as np
import cv2
from matplotlib import pyplot as plt


class Example(QMainWindow):
    
    def __init__(self):
        super().__init__()
        
        self.initUI()
        
        
    def initUI(self):      

        self.textEdit = QTextEdit()
        self.setCentralWidget(self.textEdit)
        self.statusBar()

        openFile = QAction(QIcon('open.png'), 'Open', self)
        openFile.setShortcut('Ctrl+O')
        openFile.setStatusTip('Open new File')
        openFile.triggered.connect(self.showDialog)

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(openFile)       
        
        self.setGeometry(300, 300, 350, 300)
        self.setWindowTitle('File dialog')
        self.show()
        


    def showDialog(self):

        def plot_xy(event,x,y,flags,param):
            if event == cv2.EVENT_LBUTTONDBLCLK:
                print("xy", x, y)

        fname = QFileDialog.getOpenFileName(self,
                                            'Open file',
                                            '~/PycharmProjects/Rekkari')

        if fname[0]:
            cv2.namedWindow('image')
            img = cv2.imread(fname[0],0)

            cv2.setMouseCallback('image', plot_xy)
            plt.imshow(img, cmap = 'gray', interpolation = 'bicubic')
            plt.xticks([]), plt.yticks([])  # to hide tick values on X,Y axis
            plt.show()
               
        
if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
