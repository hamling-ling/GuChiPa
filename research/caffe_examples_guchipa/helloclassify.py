import caffe

CAFFE_ROOT = os.getenv("CAFFE_ROOT")
MODEL_FILE = CAFFE_ROOT + '/examples/guchipa/lenet.prototxt'
PRETRAINED = CAFFE_ROOT + '/examples/guchipa/lenet_iter_10000.caffemodel'
IMAGE_FILE = CAFFE_ROOT + '/examples/guchipa/myimg.png'

net = caffe.Classifier(MODEL_FILE, PRETRAINED, image_dims=(28,28), raw_scale=255)
caffe.set_mode_cpu()

image = caffe.io.load_image(IMAGE_FILE, color=False)

score = net.predict([image], oversample=False)
print score
