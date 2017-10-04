import caffe
import os
import sys

CAFFE_ROOT = os.getenv("CAFFE_ROOT")

if(len(sys.argv) < 2):
    print("need image file")
    exit(1)

image_file = sys.argv[1]

image = caffe.io.load_image(image_file, color=True)

print(image.shape)
print(image)

