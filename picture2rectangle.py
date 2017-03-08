#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
1)Read selected picture
2) make rectangle to it by mouse lef button
3) by right mouse button save selected rectangle in given accuracy in pixels,
4 go for the next picture (goto 1) ).

Finnish car number plate: 118 mm x 442 mm
try here 5x20 pixel
"""

import sys
from PyQt5.QtWidgets import (QMainWindow, QTextEdit, 
    QAction, QFileDialog, QApplication, QWidget, QVBoxLayout, QPushButton, QLabel)
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

    def reset(self):
        self.refPt = []
        self.cropping = False

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


class Example(QWidget):


    def __init__(self, *args):
        super().__init__()

        self.xpixel = int(sys.argv[1])
        self.ypixel = int(sys.argv[2])
        print("INIT:", self.xpixel, self.ypixel)

        self.mouse = MouseRectangle()

        layout = QVBoxLayout()
        self.btn = QPushButton("QFileDialog static method demo")
        self.btn.clicked.connect(self.showDialog())

        layout.addWidget(self.btn)
        self.le = QLabel("Hello")

        layout.addWidget(self.le)
        self.btn1 = QPushButton("QFileDialog object")
        self.btn1.clicked.connect(self.showDialog())
        layout.addWidget(self.btn1)

        self.contents = QTextEdit()
        layout.addWidget(self.contents)
        self.setLayout(layout)
        self.setWindowTitle("File Dialog demo")

    def getNewName(self, oldname, subdir='img'):
        """
        get new filename with extra path
        """
        import os
        #dir = os.path.dirname(oldname)
        dir = os.getcwd()
        name = os.path.basename(oldname)
        #generate new dir if it doesnot exist
        newdir = dir + '/'+ subdir
        if not os.path.exists(newdir):
            os.makedirs(newdir)
        return newdir+'/'+'sample_'+name

    def showDialog(self):
        import glob
        import math
        fnames =glob.glob('*jpg')
        fnames = fnames + glob.glob('*png')
        for fname in fnames:
        #while True:
        #    fname = QFileDialog.getOpenFileName(self,
        #                                        'Open file',
        #                                        '~/PycharmProjects/Rekkari')

        #    if fname[0]:
        #        print(fname[0])
                # cv2.namedWindow('image')
        #        img = cv2.imread(fname[0],0)
                img = cv2.imread(fname,0)
                print("size:", img.shape[0], img.shape[1])
                #if (img.shape[0] > 1000):
                #    img = cv2.resize(img, (int(img.shape[0]/2), int(img.shape[1]/2)))
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
                        img = clone.copy()
                        self.mouse.reset()
                        self.mouse.set_image(image=img)

                    # if the 'c' key is pressed, break from the loop
                    elif key == ord("c"):
                        break

                # if there are two reference points, then crop the region of interest
                # from teh image and display it
                refPt = self.mouse.get_refPt()
                if len(refPt) == 2:
                    roi = clone[refPt[0][1]:refPt[1][1], refPt[0][0]:refPt[1][0]]
                    roi_scaled = cv2.resize(roi,(self.xpixel,self.ypixel))
                    newname = self.getNewName(fname,'Rectangle')
                    print(newname)
                    cv2.imwrite(newname,roi_scaled)

                    roi = clone[refPt[0][1]:refPt[1][1], refPt[0][0]:refPt[1][0]]
                    roi_scaled = cv2.resize(roi,(2*self.xpixel,2*self.ypixel))
                    newname = self.getNewName(fname,'Rectanglex2')
                    print(newname)
                    cv2.imwrite(newname,roi_scaled)

                    roi = clone[refPt[0][1]:refPt[1][1], refPt[0][0]:refPt[1][0]]
                    roi_scaled = cv2.resize(roi,(4*self.xpixel,4*self.ypixel))
                    newname = self.getNewName(fname,'Rectanglex4')
                    print(newname)
                    cv2.imwrite(newname,roi_scaled)


                    newname2 = self.getNewName(fname,'NotScaled')
                    cv2.imwrite(newname2,roi)                    
                    #cv2.imshow("ROI", roi)
                    #cv2.waitKey(0)
                    center = (int((refPt[0][0]+refPt[1][0])/2), int((refPt[0][1]+refPt[1][1])/2))
                    radius = int(0.5*math.sqrt(\
                                               (refPt[1][1]-refPt[0][1])*\
                                               (refPt[1][1]-refPt[0][1])+\
                                               (refPt[1][0]-refPt[0][0])*\
                                               (refPt[1][0]-refPt[0][0])))
                    #print("writing with added rectangle :", newname)
                    #cv2.rectangle(clone, refPt[0], refPt[1], (255, 255, 255), -2)
                    cv2.circle(clone, center, radius, (255, 255, 255), thickness=-2)
                    newname3 = self.getNewName(fname,'NegativeSamples')
                    cv2.imwrite(newname3,clone)

                # close all open windows
                cv2.destroyAllWindows()
               
        
if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    ex = Example(sys.argv)
    sys.exit(app.exec_())
