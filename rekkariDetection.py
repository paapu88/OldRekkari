import numpy as np
import cv2

rekkari_cascade = cv2.CascadeClassifier('./rekkari.xml')

#img = cv2.imread('/home/mka/Pictures/pasi2.jpg',0)
img = cv2.imread('/home/mka/Pictures/bemari.jpg')
#img = cv2.imread('/home/mka/Pictures/finlandia.png')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

#rekkaris = rekkari_cascade.detectMultiScale(img, 1.3, 5)
WINDOW_NAME = 'Image de Lena'



for scale in [1,5, 10, 15, 20, 25, 30]:
    cv2.namedWindow(WINDOW_NAME)
    cv2.startWindowThread()    
    print("scale", scale)
    rekkaris = rekkari_cascade.detectMultiScale(gray, 1.03, scale)
    clone = img.copy()


    for (x,y,w,h) in rekkaris:
        print('xywh', x,y,w,h)
        cv2.rectangle(clone,(x,y),(x+w,y+h),(0,255,0),scale)
        cv2.imshow('clone',clone)
        #roi_gray = gray[y:y+h, x:x+w]
        #roi_color = img[y:y+h, x:x+w]


    cv2.waitKey(0)
    cv2.destroyAllWindows()
