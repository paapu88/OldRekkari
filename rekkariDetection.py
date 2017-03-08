import numpy as np
import cv2

rekkari_cascade = cv2.CascadeClassifier('./rekkari.xml')

#img = cv2.imread('/home/mka/Pictures/pasi2.jpg',0)
img = cv2.imread('/home/mka/Pictures/bemari.jpg',0)
#img = cv2.imread('/home/mka/Pictures/finlandia.png')
#gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

#rekkaris = rekkari_cascade.detectMultiScale(img, 1.3, 5)
WINDOW_NAME = 'Image de Lena'



for scale in [35, 25,20,15,10,5,1]:
    cv2.namedWindow(WINDOW_NAME)
    cv2.startWindowThread()    
    print("scale", scale)
    rekkaris = rekkari_cascade.detectMultiScale(img, 1.1, scale)
    for (x,y,w,h) in rekkaris:
        cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),scale)
        #roi_gray = gray[y:y+h, x:x+w]
        #roi_color = img[y:y+h, x:x+w]

    cv2.imshow('img',img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
