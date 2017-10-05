import caffe
import os
import sys
import numpy as np
import cv2

CAFFE_ROOT = os.getenv("CAFFE_ROOT")

if(len(sys.argv) < 2):
    print("need image file")
    exit(1)

image_file = sys.argv[1]

image = caffe.io.load_image(image_file, color=True)

image=(image*255).astype(np.uint8)
#print(image.shape)
#print(image)

rolled=np.rollaxis(image,2)
s0=rolled[0,:,:]
s1=rolled[1,:,:]
s2=rolled[2,:,:]
rolled=np.array([s2,s1,s0])
print(rolled.shape)
print(rolled)

#swapped=np.roll(rolled, 1, axis=-1)
#swapped=rolled[...,[2,0,1]]
#swapped=rolled[::2,:,::2].copy()
#swapped=rolled[...,::-1]
#print(swapped.shape)
#print(swapped)
