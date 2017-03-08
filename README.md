# Rekkari
Recognition of a numberplate of a car

1) copy positive samples to positive_samples directory
(use ../../picture2rectangle.py to clip,
clipped images go to dir 'Rectangle'
accepted full images go to dir 'NotScaled'
images with rectangle replaced by ball go to dir 'NegativeSamples'
)

2) copy negative samples to negative_samples directory
you can generate more negatives by google picture search by
python3 ../../../get_google_images.py
(remember to manually remove positive figures here)
You can process files by
python3 ../../../add_balls.py
which writes to 'HumanProcessed' directory

3) find ./negative_images -iname "*.jpg" > negatives.txt
   cp PositivePicturesFromPhone/NotScaled/* positive_images/
   find ./positive_images -iname "*.jpg" > positives.txt
4)
create distorted positive samples:
perl ../opencv-haar-classifier-training/bin/createsamples.pl  positives.txt negatives.txt samples 1000 "opencv_createsamples -maxxangle 0.1 -maxyangle 0.1 -maxzangle 0.2 -maxidev 50 -w 40 -h 10"

check: opencv_createsamples -w 40 -h 10 -vec ./samples/sample_pos4.jpg.vec

5)
merge positive *.vec files to one vec file
python2 ~/Dropbox/Apu/mergevec.py -v samples -o positives.vec
#python2 ../opencv-haar-classifier-training/tools/mergevec.py -v samples -o positives.vec
check: opencv_createsamples -w 40 -h 10 -vec positives.vec

4) generate vec file of positive samples
NOT USED
cp positives.txt  info.txt
edit info.txt to contain pixel info
> ./positive_images/sample_IMG_20170307_102910.jpg 1 0 0 80 20
> ...
opencv_createsamples -num 36 -info info.txt -w 80 -h 20 -vec positives.vec

6) train:
check: opencv_createsamples -w 40 -h 10 -vec positives.vec
rm -f classifier/*
mkdir classifier
opencv_traincascade -data classifier -vec positives.vec -bg negatives.txt\
  -numStages 50 -minHitRate 0.999 -maxFalseAlarmRate 0.5 -numPos 1000 \
  -numNeg 429 -w 40 -h 10 -mode ALL -precalcValBufSize 512\
  -precalcIdxBufSize 512

7) in rekkariDetection.py play with parameters
rekkari_cascade.detectMultiScale(img, 1.1, scale)
