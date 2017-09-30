import caffe
import os
import sys

CAFFE_ROOT = os.getenv("CAFFE_ROOT")
MODEL_FILE = CAFFE_ROOT + '/examples/lelenet_bg_gray28/lenet.prototxt'
PRETRAINED = CAFFE_ROOT + '/examples/lelenet_bg_gray28/lenet_iter_10000.caffemodel'

if(len(sys.argv) < 2):
    print("need image file")
    exit(1)

image_file = sys.argv[1]

net = caffe.Classifier(MODEL_FILE, PRETRAINED, image_dims=(28,28), raw_scale=255)
caffe.set_mode_cpu()
#caffe.set_mode_gpu()

image = caffe.io.load_image(image_file, color=False)
print(image.shape)

score = net.predict([image], oversample=False)
print score
