import sys
import caffe
import numpy as np
from PIL import Image as image
import lmdb
import cv2

caffe_root = '/home/pixela/GitHub/caffe'

MODEL_FILE = caffe_root + '/examples/guchipa/lenet.prototxt'
PRETRAINED = caffe_root + '/examples/guchipa/lenet_iter_10000.caffemodel'

#net = caffe.Net(MODEL_FILE, PRETRAINED,caffe.TEST)
#caffe.set_mode_cpu()


db_path = caffe_root + '/examples/guchipa/mnist_train_lmdb'
lmdb_env = lmdb.open(db_path)
lmdb_txn = lmdb_env.begin()
lmdb_cursor = lmdb_txn.cursor()
count = 0
correct = 0

for key, value in lmdb_cursor:
	count = count+1
	if count > 15:
		break

datum = caffe.proto.caffe_pb2.Datum()
datum.ParseFromString(value)
label = int(datum.label)

image = caffe.io.datum_to_array(datum)
image = image.astype(np.uint8)

data=np.asarray([image])
a=data[0][0]
print "label=", label


for i in range(0, 28):
	for j in range(0, 28):
		sys.stdout.write("{0:02X}".format(a[i,j]))
		sys.stdout.write(" ")
	print ""
