import sys
import os
import caffe
import numpy as np
from PIL import Image as image
import lmdb
import cv2

caffe_root = os.getenv("CAFFE_ROOT")

db_path = caffe_root + '/examples/lelenet_bg/train_lmdb'
if(len(sys.argv) < 2):
    print("need bin file and index")
    exit(1)

db_path = sys.argv[1]
img_idx = int(sys.argv[2])

lmdb_env = lmdb.open(db_path)
lmdb_txn = lmdb_env.begin()
lmdb_cursor = lmdb_txn.cursor()
count = 0

for key, value in lmdb_cursor:
	count = count+1
	if count > img_idx:
		break

datum = caffe.proto.caffe_pb2.Datum()
datum.ParseFromString(value)
label = int(datum.label)

image = caffe.io.datum_to_array(datum)
image = image.astype(np.uint8)

print(image.shape)

data=np.asarray([image])
a=data[0][0]
print "label=", label

fn = "{0}.png".format(img_idx)
image=np.transpose(image, (1,2,0))
cv2.imwrite(fn, image)
print("{0} saved".format(fn))

#for i in range(0, 64):
#	for j in range(0, 28):
#		sys.stdout.write("{0:02X}".format(a[i,j]))
#		sys.stdout.write(" ")
#	print ""
