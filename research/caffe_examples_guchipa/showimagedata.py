import sys
import caffe
import numpy as np
from PIL import Image as image
import lmdb
import os

CAFFE_ROOT = os.environ['CAFFE_ROOT']

db_path = CAFFE_ROOT + '/examples/guchipa/train_lmdb'
#db_path = CAFFE_ROOT + '/examples/guchipa/test_lmdb'

lmdb_env = lmdb.open(db_path)
lmdb_txn = lmdb_env.begin()
lmdb_cursor = lmdb_txn.cursor()

wanted_image_idx = 0
print sys.argv
if(len(sys.argv) > 1) :
        wanted_image_idx = int(sys.argv[1])

count = 0
for key, value in lmdb_cursor:
	count = count+1
	if count == wanted_image_idx:
		break

datum = caffe.proto.caffe_pb2.Datum()
datum.ParseFromString(value)
label = int(datum.label)

image = caffe.io.datum_to_array(datum)
image = image.astype(np.uint8)

data=np.asarray([image])
a=data[0][0]
print "image[{0}], label={1}".format( wanted_image_idx, label)


for i in range(0, 28):
	for j in range(0, 28):
		sys.stdout.write("{0:02X}".format(a[i,j]))
		sys.stdout.write(" ")
	print ""
