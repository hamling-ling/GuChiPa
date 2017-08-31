import sys
import caffe
import numpy as np
from PIL import Image as image
import lmdb
import cv2

caffe_root = '/home/pixela/GitHub/caffe'

MODEL_FILE = caffe_root + '/examples/guchipa/lenet.prototxt'
PRETRAINED = caffe_root + '/examples/guchipa/lenet_iter_10000.caffemodel'
IMAGE_FILE = caffe_root + '/python/four.png'

print "image=", IMAGE_FILE

net = caffe.Net(MODEL_FILE, PRETRAINED,caffe.TEST)
caffe.set_mode_cpu()


db_path = caffe_root + '/examples/guchipa/mnist_train_lmdb'

inputs = caffe.io.load_image( IMAGE_FILE, color=False)

print inputs.shape

data=np.zeros([1,1,28,28])
data[0,0,:,:] = inputs[:,:,0] * 255
data = data.astype(np.uint8)

a=data[0][0]

for i in range(0, 28):
	for j in range(0, 28):
		sys.stdout.write("{0:02X}".format(a[i,j]))
		sys.stdout.write(" ")
	print ""
