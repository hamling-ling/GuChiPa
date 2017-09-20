import cv2
import os
import sys
import numpy as np

data_size = 28*28+1

if(len(sys.argv) < 2):
    print("need bin file and index")
    exit(1)

bin_file = sys.argv[1]
bin_idx = int(sys.argv[2])

f = open(bin_file, "rb")
f.seek(bin_idx * data_size, os.SEEK_SET)

img = np.fromfile(f, dtype=np.dtype('uint8'), count=28*28)
img = img.reshape(28,28)

lbl = np.fromfile(f, dtype=np.dtype('uint8'), count=1)

print("label={0}".format(lbl[0]))

for i in range(0, 28):
    for j in range(0, 28):
	sys.stdout.write("{0:02X}".format(img[i,j]))
	sys.stdout.write(" ")
    print ""

fn = "{0}.png".format(bin_idx)
cv2.imwrite(fn, img)
print("{0} saved".format(fn))
