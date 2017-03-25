"""
python3 ~/PycharmProjects/Rekkari/video2images.py "Rekisteri_4_short.mp4"
Functions related to read and write videos and images in opencv

"""


import cv2
import numpy as np
import sys



class VideoIO():
    def __init__(self, videoFileName=None, fps=24, first_frame=0, last_frame=None, colorChange=cv2.COLOR_YUV2GRAY_420):

        self.fps = fps
        self.videoFileName = videoFileName
        #self.cap = cv2.VideoCapture(*args)
        self.first_frame = first_frame
        self.last_frame = last_frame
        self.colorChange=colorChange
        self.n_frames=None
        self.frames=None
        print ("INIT OK")

    def readVideoFrames(self, videoFileName=None):
        """ read in frames and convert to desired format"""
        if videoFileName is None:
            videoFileName = self.videoFileName
        if self.first_frame is None:
            first_frame = 0
        else:
            first_frame = self.first_frame
        last_frame = self.last_frame

        print ("starting reading: filename", videoFileName)
        cap = cv2.VideoCapture(videoFileName)
        while not cap.isOpened():
            cap = cv2.VideoCapture(videoFileName)
            cv2.waitKey(1000)
            print("Wait for the header")

        print("self:", last_frame)
        if last_frame is None:
            last_frame = cap.get(cv2.CAP_PROP_FRAME_COUNT)
            print("LAST NR", )
        self.frames = []

        cap.set(cv2.CAP_PROP_POS_FRAMES, first_frame)
        while True:
            flag, frame = cap.read()
            if flag:
                gray = cv2.cvtColor(frame, self.colorChange)
                self.frames.append(gray)
                pos_frame = cap.get(cv2.CAP_PROP_POS_FRAMES)
                print (str(pos_frame)+" frames")
            else:
                # The next frame is not ready, so we try to read it again
                cap.set(cv2.CAP_PROP_POS_FRAMES, pos_frame-1)
                print("frame is not ready")
                # It is better to wait for a while for the next frame to be ready
                cv2.waitKey(1000)

            k = cv2.waitKey(0) & 0xFF
            if k == 27:
                break
            if cap.get(cv2.CAP_PROP_POS_FRAMES) == last_frame+1:
                # If the number of captured frames is equal to the total number of frames,
                # we stop
                break



        self.n_frames=last_frame-first_frame+1
        cap.release()
        print("finished reading")

    def setColorChange(self, colorChange):
        self.colorChange = colorChange


    def writeAllImages(self, format='jpg', prefix=''):
        """Write given frames to disk as images one-by-one"""

        for i, frame in enumerate(self.frames):
            cv2.imwrite(prefix+'.'+str(i+self.first_frame)+'.'+format, frame)



if __name__ == '__main__':
    import sys
    videoFileName=sys.argv[1]
    video2images = VideoIO(videoFileName=videoFileName,first_frame=100, last_frame=120, colorChange=cv2.COLOR_YUV2GRAY_420)
    video2images.readVideoFrames(videoFileName=videoFileName)
    video2images.writeAllImages(prefix=videoFileName)




