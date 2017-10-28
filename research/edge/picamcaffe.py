import caffe
from caffe.proto import caffe_pb2
import os
import sys
import cv2
import numpy as np
import pygame
import picamera
from picamera.array import PiRGBArray
import time

CAFFE_IMAGE_WIDTH = 64
CAFFE_IMAGE_HEIGHT = 64
FILE_PATH=os.path.dirname(os.path.realpath(__file__))
DEEPLEARNING_ROOT=os.path.realpath(FILE_PATH + '/../deeplearning-lelenet')
print("DEEPLEARNING_ROOT=" + DEEPLEARNING_ROOT)

CAFFE_ROOT = os.getenv("CAFFE_ROOT")
MODEL_FILE = DEEPLEARNING_ROOT + '/caffe_models/caffemodel_alelenet/caffenet_deploy_1.prototxt'
PRETRAINED = DEEPLEARNING_ROOT + '/caffe_models/caffemodel_alelenet/caffe_model_1_iter_10000.caffemodel'
MEAN_FILE  = DEEPLEARNING_ROOT + '/input/mean.binaryproto'

CAMERA_WIDTH = 320
CAMERA_HEIGHT = 240
raw = None
cam = None

gamma1 = 0.5
LUT_G1 = np.arange(256, dtype = 'uint8' )
for i in range(256):
    LUT_G1[i] = 255 * pow(float(i) / 255, 1.0 / gamma1)

def initCaffe():
    mean_blob = caffe_pb2.BlobProto()
    mean_array = None
    with open(MEAN_FILE) as f:
        mean_blob.ParseFromString(f.read())
        mean_array = np.asarray(mean_blob.data, dtype=np.float32).reshape(
                    (mean_blob.channels, mean_blob.height, mean_blob.width))

    net = caffe.Net(MODEL_FILE, PRETRAINED,
                    caffe.TEST)
    caffe.set_mode_cpu()

    #Define image transformers
    transformer = caffe.io.Transformer({'data': net.blobs['data'].data.shape})
    transformer.set_mean('data', mean_array)
    transformer.set_transpose('data', (2,0,1))
    
    return net, transformer

def initCv():
    camera = picamera.PiCamera()
    camera.resolution = (CAMERA_WIDTH, CAMERA_HEIGHT)
    camera.led = True
    camera.framerate = 32
    rawCap = PiRGBArray(camera, size=(CAMERA_WIDTH, CAMERA_HEIGHT))

    #warm up
    time.sleep(0.1)

    return camera, rawCap

def initSnd():
    pygame.mixer.init()
    snd_g = pygame.mixer.Sound('snd/g.wav')
    snd_c = pygame.mixer.Sound('snd/c.wav')
    snd_a = pygame.mixer.Sound('snd/a.wav')
    return [snd_g, snd_c, snd_a]

def cropImg(img):
    width = img.shape[1]
    height = img.shape[0]
    offset = (width-height)/2
    edge_len=height

    crop_img = img[0:edge_len, offset:offset+edge_len, :]
    
    return crop_img

def transform_img(img, img_width=CAFFE_IMAGE_WIDTH, img_height=CAFFE_IMAGE_HEIGHT):    
    #Histogram Equalization
    img[:, :, 0] = cv2.equalizeHist(img[:, :, 0])
    img[:, :, 1] = cv2.equalizeHist(img[:, :, 1])
    img[:, :, 2] = cv2.equalizeHist(img[:, :, 2])

    #Image Resizing
    img = cv2.resize(img, (img_width, img_height), interpolation = cv2.INTER_CUBIC)

    return img

def predict(img, trs):
    # warok around
    img_path = '/tmp/tmp.jpg'
    cv2.imwrite(img_path, img)
    img = cv2.imread(img_path, cv2.IMREAD_COLOR)
    img = transform_img(img, img_width=CAFFE_IMAGE_WIDTH, img_height=CAFFE_IMAGE_HEIGHT)

    net.blobs['data'].data[...] = trs.preprocess('data', img)
    out = net.forward()
    score = out['prob']
    
    return score[0]

def playSound(score, last_snd):
    index = 0
    if(score0[0] > 0.9):
        index = 0
    elif(score0[1] > 0.9):
        index = 1
    elif(score0[2] > 0.9):
        index = 2
    else:
        index = 3

    if(index < 3 and last_snd != index):
        sns[index].play()
    
    return index

def handleKeyInput():
    key = cv2.waitKey(1)
    #print("key is {0}".format(key))
    
    # enter to capture still
    if key == 10:
        filename = "out{0}.jpg".format(counter)
        ret = cv2.imwrite(filename, img)
        print(str(ret) + " " + filename)
        counter = counter + 1
    # q to exit
    elif key == ord('q'):
        return True
    return False

net, trans  = initCaffe()
cam, raw = initCv()
sns = initSnd()

counter = 0
last_snd = 3

for frame in cam.capture_continuous(raw, format="bgr", use_video_port=True):

    img = frame.array
    img = cropImg(img)
    cv2.imshow('camera', img)

    score0 = predict(img,trans)
    print(score0)

    last_snd = playSound(score0, last_snd)

    if(handleKeyInput()):
        break
    raw.truncate(0)

cam.led = False
cv2.destroyAllWindows()
