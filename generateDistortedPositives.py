"""
# python3 ./generateDistortedPositives.py -infiles 'sample_pos*'
python3 ../../generateDistortedPositives.py -infiles 'sample_pos*' 

Check with 
opencv_createsamples -w 80 -h 20 -vec merged.vec
"""


import argparse
import glob
import os
import shutil
import subprocess
import mergevec
import sys

parser = argparse.ArgumentParser()

parser.add_argument('-infiles', action='store', dest='infiles',
                    help='filenames of positive images')
parser.add_argument('-width', action='store', dest='width', 
                    help='width of image in pixels', default='80')
parser.add_argument('-height', action='store', dest='height', 
                    help='height of image in pixels', default='20')
parser.add_argument('-maxxangle', action='store', dest='maxxangle', 
                    help='maxrot x', default='0.3')
parser.add_argument('-maxyangle', action='store', dest='maxyangle', 
                    help='maxrot y', default='0.3')
parser.add_argument('-maxzangle', action='store', dest='maxzangle', 
                    help='maxrot z',  default='0.5')
args = parser.parse_args()

cwd = os.getcwd()
vecdir = cwd+'/VecFilesTmp'
print(vecdir)
try:
    shutil.rmtree(vecdir)
except:
    pass
os.makedirs(vecdir)
names=glob.glob(args.infiles)
print(names)

#generate shaken&stirren new positive samples in vec files
for i, name in enumerate(names):
    command = 'opencv_createsamples -vec ' + vecdir+'/'+str(i)+'vec.vec ' +\
              '-img ' + name + ' ' +\
              '-maxxangle ' + args.maxxangle + ' ' +\
              '-maxyangle ' + args.maxyangle + ' ' +\
              '-maxzangle ' + args.maxzangle + ' ' +\
              '-w ' + args.width + ' ' +\
              '-h ' + args.height + ' '
    subprocess.call(command, shell=True)

# merge vec files
subprocess.call('python ~/Dropbox/Apu/mergevec.py -v VecFilesTmp -o merged.vec', shell=True)
#submergevec.merge_vec_files('VecFilesTmp', 'merged.vec')

