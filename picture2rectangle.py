# python3 picture2rectangle.py 10 15
# in a directory containing only jpg (png) files
# the arguments are initial box size in x and y
"""
1) Read selected picture (automated)
2) make rectangle to it by mouse lef button
3) the dimension of x is forced by fixed ratio
4) you can move the rectancle by up=w down=z left=a right=d, bigger=+, smaller=-
5) when ready you can mouse click another plate or
6) when done press c if mistakes press r and start picture again

Various resolutions are in directories Rectangle*
unscaled samples with original resolution of the rectangle box are in dir NotScaled
Negative samples are in dir NegativeSamples (they have white ball on top of plates)


Finnish car number plate: 118 mm x 442 mm

"""

import sys
from PyQt5.QtWidgets import QMainWindow, QTextEdit, \
    QAction, QFileDialog, QApplication, QWidget, \
    QVBoxLayout, QPushButton, QLabel
from PyQt5.QtGui import QIcon
import numpy as np
import cv2
from matplotlib import pyplot as plt

class MouseRectangle():
    """ get a rectangle by mouse"""
    def __init__(self):
        #super().__init__()
        self.refPts = []
        self.cropping = False
        self.image = None
        self.ratio = None

    def set_image(self, image):
        self.image = image

    def reset(self):
        self.refPts = []
        self.cropping = False

    def get_refPts(self):
        return self.refPts

    def set_refPts(self, refPts):
        self.refPts = refPts

    def set_ratio(self, ratio):
        """self y/x ratio for the selection box"""
        if self.ratio is not None:
            self.ratio = ratio
        else:
            # assume long eu plates
            self.ratio = 442/118

    def get_ratio(self):
        return self.ratio

    def plot_xy(self,event,x,y,flags,param):
        if event == cv2.EVENT_LBUTTONDBLCLK:
            print("xy", x, y)

    def click_and_crop(self,event, x, y, flags, param):
	    # grab references to the global variables

        # if the left mouse button was clicked, record the starting
        # (x, y) coordinates and indicate that cropping is being
        # performed
        if event == cv2.EVENT_LBUTTONDOWN:
            self.refPts.append([x, y])
            self.cropping = True
            print("S1", self.refPts)

        # check to see if the left mouse button was released
        elif event == cv2.EVENT_LBUTTONUP:
            # record the ending (x, y) coordinates and indicate that
            # the cropping operation is finished

            # set the ratio of the rectangle to be correct
            if self.ratio is not None:
                dy = y - self.refPts[-1][1]
                x = self.refPts[-1][0]+ int(self.ratio * dy)

            self.refPts.append([x, y])
            self.cropping = False

            # draw a rectangle around the region of interest
            print("MOUSE UP", self.refPts)
            for i in range(0,len(self.refPts),2):
                print('pts', self.refPts[i])
                cv2.rectangle(self.image, tuple(self.refPts[i]), tuple(self.refPts[i+1]), (0, 255, 255), 1)

            #cv2.rectangle(self.image, tuple(self.refPts[0]), tuple(self.refPts[1]), (0, 255, 255), 5)
            cv2.imshow("image", self.image)


class Example(QWidget):


    def __init__(self, *args):
        super().__init__()

        try:
            self.xpixel = int(sys.argv[1])
            self.ypixel = int(sys.argv[2])
        except:
            print("setting default values for pixels")
            self.xpixel = 40
            self.ypixel = 10
        print("INIT:", self.xpixel, self.ypixel)

        self.mouse = MouseRectangle()
        self.mouse.set_ratio(self.xpixel/self.ypixel)

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

    def saveImage(self, image, ratio, fname):
        import math
        # if there are two reference points, then crop the region of interest
        # from teh image and display it
        refPts = self.mouse.get_refPts()
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # plot all plates to directories, first with native resolution , then in different resolutions
        for i in range(0, len(refPts), 2):
            newname = self.getNewName(fname, 'NotScaled')
            clone = gray.copy()
            roi = clone[refPts[i][1]:refPts[i+1][1], refPts[i][0]:refPts[i+1][0]]
            cv2.imwrite(newname, roi)
            for ypixel in range(self.ypixel, self.ypixel + 50, 1):
                xpixel = int(ypixel * ratio)
                clone = gray.copy()
                roi = clone[refPts[i][1]:refPts[i+1][1], refPts[i][0]:refPts[i+1][0]]
                print("SC:",xpixel, ypixel,refPts[i][1],refPts[i+1][1], refPts[i][0],refPts[i+1][0])
                roi_scaled = cv2.resize(roi, (xpixel, ypixel))
                newname = self.getNewName(fname, 'Rectangle'+'-'+str(xpixel)+'-'+str(ypixel))
                cv2.imwrite(newname, roi_scaled)

        # save negative sample with ball on top of all plates
        clone = gray.copy()
        for i in range(0, len(refPts), 2):
            center = (int((refPts[i][0] + refPts[i+1][0]) / 2), int((refPts[i][1] + refPts[i+1][1]) / 2))
            radius = int(0.5 * math.sqrt( \
                (refPts[i][1] - refPts[i+1][1]) * \
                (refPts[i][1] - refPts[i+1][1]) + \
                (refPts[i][0] - refPts[i+1][0]) * \
                (refPts[i][0] - refPts[i+1][0])))
            # print("writing with added rectangle :", newname)
            # cv2.rectangle(clone, refPts[0], refPts[1], (255, 255, 255), -2)
            cv2.circle(clone, center, radius, (255, 255, 255), thickness=-2)
        newname3 = self.getNewName(fname, 'NegativeSamples')
        cv2.imwrite(newname3, clone)

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
                #plt.imshow(img, cmap = 'gray', interpolation = 'bicubic')
                #plt.xticks([]), plt.yticks([])  # to hide tick values on X,Y axis
                #plt.show()
                #cv2.imshow('image', img)
                #cv2.waitKey(0)
                #sys.exit()
                #if (img.shape[0] > 1000):
                #    img = cv2.resize(img, (int(img.shape[0]/2), int(img.shape[1]/2)))
                clone = img.copy()
                self.mouse.set_image(image=img)

                #cv2.setMouseCallback('image', plot_xy)
                #cv2.setMouseCallback('image', self.mouse.plot_xy)
                #cv2.setMouseCallback('image', self.mouse.click_and_crop)

                print("still alive 1")

                # keep looping until the 'q' key is pressed
                while True:
                    # display the image and wait for a keypress
                    print("still alive 2")
                    cv2.imshow("image", img)
                    print("still alive 3")
                    key = cv2.waitKey(33) & 0xFF
                    print("still alive 4")
                    change = False
                    # if the 'r' key is pressed, reset the cropping region
                    if key == ord("r"):
                        img = clone.copy()
                        self.mouse.reset()
                        self.mouse.set_image(image=img)

                    elif key == ord("+"):
                        refPts = self.mouse.get_refPts()
                        refPts[-2][0]= refPts[-2][0] - 1
                        refPts[-2][1]= refPts[-2][1] - 1
                        refPts[-1][0] = refPts[-1][0] + 1
                        refPts[-1][1] = refPts[-1][1] + 1
                        self.mouse.set_refPts(refPts)
                        change = True
                    elif key == ord("-"):
                        refPts = self.mouse.get_refPts()
                        refPts[-2][0] = refPts[-2][0] + 1
                        refPts[-2][1] = refPts[-2][1] + 1
                        refPts[-1][0] = refPts[-1][0] - 1
                        refPts[-1][1] = refPts[-1][1] - 1
                        self.mouse.set_refPts(refPts)
                        change = True
                    elif key == ord("w"):
                        #up
                        refPts = self.mouse.get_refPts()
                        refPts[-2][1] = refPts[-2][1] - 1
                        refPts[-1][1] = refPts[-1][1] - 1
                        self.mouse.set_refPts(refPts)
                        change = True
                    elif key == ord("z"):
                        #up
                        refPts = self.mouse.get_refPts()
                        refPts[-2][1] = refPts[-2][1] + 1
                        refPts[-1][1] = refPts[-1][1] + 1
                        self.mouse.set_refPts(refPts)
                        change = True
                    elif key == ord("d"):
                        #up
                        refPts = self.mouse.get_refPts()
                        refPts[-2][0] = refPts[-2][0] + 1
                        refPts[-1][0] = refPts[-1][0] + 1
                        self.mouse.set_refPts(refPts)
                        change = True
                    elif key == ord("a"):
                        #up
                        refPts = self.mouse.get_refPts()
                        refPts[-2][0] = refPts[-2][0] - 1
                        refPts[-1][0] = refPts[-1][0] - 1
                        self.mouse.set_refPts(refPts)
                        change = True

                    # if the 'c' key is pressed, break from the loop
                    elif key == ord("c"):
                        break
                    #print(key)
                    if change:
                        change = False
                        img = clone.copy()
                        for i in range(0,len(refPts),2):
                            cv2.rectangle(img, tuple(refPts[i]), tuple(refPts[i+1]), (0, 255, 255), 1)
                        self.mouse.set_image(image=img)

                self.saveImage(clone.copy(), self.mouse.get_ratio(), fname)
                self.mouse.reset()

                # close all open windows
                cv2.destroyAllWindows()
               
        
if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    ex = Example(sys.argv)
    sys.exit(app.exec_())
