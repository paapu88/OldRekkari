""" read in figure, scan it, get lots of small images to be analysed whether they contain a character/number"""

import numpy as np
import cv2

# idendify rekkari.jpeg gives 259X194


# Load an color image in grayscale
#img = cv2.imread('rekkari.jpeg',0)

#cv2.imshow('image',img)
#cv2.waitKey(0)
#cv2.destroyAllWindows()

# load and show video
cap = cv2.VideoCapture('/home/mka/Downloads/test.mp4')
frames = []
while(cap.isOpened()):
    ret, frame = cap.read()
    try:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frames.append(gray)
    except:
        break
cap.release()

myframe=frames[100]
cv2.line(myframe,(0,0),(511,511),(255,0,0),5)
cv2.rectangle(myframe,(384,0),(510,128),(0,255,0),3)
cv2.circle(myframe,(447,63), 63, (0,0,255), -1)

# Create a black image, a window
img = np.zeros((720,1280,3), np.uint8)
img[:,:,0] = myframe
cv2.namedWindow('image')
#np.expand_dims(myframe, axis=0)
#print(myframe.shape)

# myframe.reshape(myframe.shape + (4,))
def nothing(x):
    pass

#

# create trackbars for color change
cv2.createTrackbar('R','image',0,255,nothing)
cv2.createTrackbar('G','image',0,255,nothing)
cv2.createTrackbar('B','image',0,255,nothing)

# create switch for ON/OFF functionality
switch = '0 : OFF \n1 : ON'
cv2.createTrackbar(switch, 'image',0,1,nothing)

while(1):
    cv2.imshow('image', img)
    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break

    # get current positions of four trackbars
    r = cv2.getTrackbarPos('R','image')
    g = cv2.getTrackbarPos('G','image')
    b = cv2.getTrackbarPos('B','image')
    s = cv2.getTrackbarPos(switch,'image')

    if s == 0:
        img[:] = 0
    else:
        img[:] = [b,g,r]

cv2.waitKey(0)
cv2.destroyAllWindows()
