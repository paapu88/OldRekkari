# Rekkari
Recognition of a numberplate of a car


1 --------- hand-made positive samples -----------------------
# first generate positive samples to dir 'img' by program picture2matplotlib.py
(hand picking rectangles containing a number plate)

2 -------- more positive samples by distortions -------------------------
# 10 positive samples in ~/PycharmProjects/Rekkari/Training/img/sample_pos*
# they are rotated and blurred by
# python3 ../../generateDistortedPositives.py -infiles 'sample_pos*'
# which generates a big positive-sample vec file 'merged.vec'
# the default values is to generate 1000 pictures from the original one, so we get total 10000 positive samples

3 -------- taking fotos and making slices: negative samples ----------------

Take random fotos about 50 on the street (no number plates)
Upload to google drive from mobile phone, download from googledrive to computer,
here to dir ~/PycharmProjects/Rekkari/Training/Negative/NegativesSmall  (*jpg files)

generate small slices that are of the same size as positive samples (here dx=20pix, dy=80pix):
~/PycharmProjects/Rekkari/Training/Negative/NegativesSmall$ python3 ../../generateNegatives.py -infiles '*jpg'

~/PycharmProjects/Rekkari/Training$ find ./Negative/NegativesSmall/ -iname "*.jpg" > negatives.txt

3b ----------- too many samples (memory problem) -------------------
# reduce the number of negative samples by sampling selected amount of negative samples:
~/PycharmProjects/Rekkari/Training/Negative/NegativesSmall> python3 ../../../subSampleRandomNegatives.py -infiles '*jpg' -nrandom 20000
This writes 20000 files to dir ./Negativesrandom20000

4 --------- Train the classifier --------------

mkdir classifier   # otherwise you get error Parameters can not be written, because file classifier/params.xml can not be opened.

Kauppi:~/PycharmProjects/Rekkari/Training>
opencv_traincascade -data classifier -vec ./img/merged.vec -bg negatives.txt \
-numStages 20 -minHitRate 0.999 -maxFalseAlarmRate 0.5 -numPos 10000 \
-numNeg 66092 -w 80 -h 20 -mode ALL -precalcValBufSize 128 -precalcIdxBufSize 128

mka@mka-HP:~/PycharmProjects/Rekkari/Training10000$ opencv_traincascade -data classifier -vec merged.vec -bg negatives.txt\
>   -numStages 20 -minHitRate 0.999 -maxFalseAlarmRate 0.5 -numPos 1000 \
>     -numNeg 10000 -w 80 -h 20 -mode ALL
