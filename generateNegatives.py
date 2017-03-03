"""
# python3 ./generateNegatives.py -infiles '*jpg'
python3 ../../generateDistortedPositives.py -infiles 'sample_pos*' 

Check with 
opencv_createsamples -w 80 -h 20 -vec merged.vec
"""


import argparse
import glob
import os
import shutil
import cv2
import sys
import numpy as np

parser = argparse.ArgumentParser()

parser.add_argument('-infiles', action='store', dest='infiles',
                    help='filenames of positive images')
parser.add_argument('-width', action='store', dest='width', 
                    help='width of image in pixels', default=80, type=int)
parser.add_argument('-height', action='store', dest='height', 
                    help='height of image in pixels', default=20, type=int)
args = parser.parse_args()

cwd = os.getcwd()
vecdir = cwd+'/NegativesSmall'
print(vecdir)

try:
    os.makedirs(vecdir)
except:
    pass

names=glob.glob(args.infiles)
print(names)

#generate slices of original pictures (to be negative samples)
for i, name in enumerate(names):
    img = cv2.imread(name,0)
    big_picture_height, big_picture_width = img.shape
    for i,ix in enumerate(np.arange(0, big_picture_width, args.width)):
        for j, jy in enumerate(np.arange(0, big_picture_height, args.height)):
            small_picture = img[jy:jy+args.height, ix:ix+args.width]
            cv2.imwrite(vecdir+'/small_'+str(jy)+'-'+str(ix)+name,small_picture)

