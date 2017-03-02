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

class MouseRectangle():
    """ get a rectangle by mouse"""
    def __init__(self):
        #super().__init__()
        self.refPt = []
        self.cropping = False
        self.image = None

    def set_image(self, image):
        self.image = image

    def get_refPt(self):
        return self.refPt

    def plot_xy(self,event,x,y,flags,param):
        if event == cv2.EVENT_LBUTTONDBLCLK:
            print("xy", x, y)

    def click_and_crop(self,event, x, y, flags, param):
	    # grab references to the global variables

        # if the left mouse button was clicked, record the starting
        # (x, y) coordinates and indicate that cropping is being
        # performed
        if event == cv2.EVENT_LBUTTONDOWN:
            self.refPt = [(x, y)]
            self.cropping = True

        # check to see if the left mouse button was released
        elif event == cv2.EVENT_LBUTTONUP:
            # record the ending (x, y) coordinates and indicate that
            # the cropping operation is finished
            self.refPt.append((x, y))
            self.cropping = False

            # draw a rectangle around the region of interest
            cv2.rectangle(self.image, self.refPt[0], self.refPt[1], (0, 255, 0), 2)
            cv2.imshow("image", self.image)


class Example(QMainWindow):
    
    def __init__(self):
        super().__init__()
        
        self.initUI()
        self.mouse = MouseRectangle()
        
        
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

        #def plot_xy(event,x,y,flags,param):
        #    if event == cv2.EVENT_LBUTTONDBLCLK:
        #        print("xy", x, y)


        fname = QFileDialog.getOpenFileName(self,
                                            'Open file',
                                            '~/PycharmProjects/Rekkari')

        if fname[0]:
            # cv2.namedWindow('image')
            img = cv2.imread(fname[0],0)
            clone = img.copy()
            self.mouse.set_image(image=img)
            cv2.imshow('image', img)

            #cv2.setMouseCallback('image', plot_xy)
            #cv2.setMouseCallback('image', self.mouse.plot_xy)
            cv2.setMouseCallback('image', self.mouse.click_and_crop)

            #plt.imshow(img, cmap = 'gray', interpolation = 'bicubic')
            #plt.xticks([]), plt.yticks([])  # to hide tick values on X,Y axis
            #plt.show()

            # keep looping until the 'q' key is pressed
            while True:
                # display the image and wait for a keypress
                cv2.imshow("image", img)
                key = cv2.waitKey(1) & 0xFF

                # if the 'r' key is pressed, reset the cropping region
                if key == ord("r"):
                    image = clone.copy()

                # if the 'c' key is pressed, break from the loop
                elif key == ord("c"):
                    break

            # if there are two reference points, then crop the region of interest
            # from teh image and display it
            refPt = self.mouse.get_refPt()
            if len(refPt) == 2:
                roi = clone[refPt[0][1]:refPt[1][1], refPt[0][0]:refPt[1][0]]
                cv2.imshow("ROI", roi)
                cv2.waitKey(0)

            # close all open windows
            cv2.destroyAllWindows()
               
        
if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
