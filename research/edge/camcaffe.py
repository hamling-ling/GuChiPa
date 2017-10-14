import caffe
import os
import sys
import cv2
import numpy as np
import pygame

CAFFE_IMG_WIDTH = 64
CAFFE_IMG_HEIGHT = 64
FILE_PATH=os.path.dirname(os.path.realpath(__file__))
DEEPLEARNING_ROOT=os.path.realpath(FILE_PATH + '/../deeplearning-lelenet')
print("DEEPLEARNING_ROOT=" + DEEPLEARNING_ROOT)

CAFFE_ROOT = os.getenv("CAFFE_ROOT")
MODEL_FILE = DEEPLEARNING_ROOT + '/caffe_models/caffemodel_alelenet/caffenet_deploy_1.prototxt'
PRETRAINED =DEEPLEARNING_ROOT + '/caffe_models/caffemodel_alelenet/caffe_model_1_iter_5000.caffemodel'



gamma1 = 0.5
LUT_G1 = np.arange(256, dtype = 'uint8' )
for i in range(256):
    LUT_G1[i] = 255 * pow(float(i) / 255, 1.0 / gamma1)

def initCaffe():
    net = caffe.Classifier(MODEL_FILE, PRETRAINED, image_dims=(64,64), raw_scale=255)
    caffe.set_mode_cpu()
    #caffe.set_mode_gpu()
    return net

def initCv():
    capture = cv2.VideoCapture(0)
    capture.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH,320);
    capture.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT,240);

    return capture

def initSnd():
    pygame.mixer.init()
    snd_g = pygame.mixer.Sound('snd/g.wav')
    snd_c = pygame.mixer.Sound('snd/c.wav')
    snd_a = pygame.mixer.Sound('snd/a.wav')
    return [snd_g, snd_c, snd_a]

def cvtImg(img):
    #img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

    width = img.shape[1]
    height = img.shape[0]
    offset = (width-height)/2
    edge_len=height
    
    crop_img = img[0:edge_len, offset:offset+edge_len, :]

    #img = cv2.LUT(img, LUT_G1)
    cv2.imshow('camera', crop_img)
    
    scaled_img = cv2.resize(crop_img,(CAFFE_IMG_WIDTH,CAFFE_IMG_HEIGHT))
    #print("resized shape={0}".format(img.shape))
    scaled_img = np.reshape(scaled_img,(CAFFE_IMG_WIDTH,CAFFE_IMG_HEIGHT,3))
    
    return scaled_img

def readImg():
    img=None
    for i in range(5):
        ret,img=cap.read(0)
    
    ret,img = cap.read(0)
    if ret == False:
        print("read image failed")

    return ret, img

def predict(cvImg):
    tmpImg1 = cvImg/255.0
    caffImg = tmpImg1[:,:,(2,1,0)]
    
    score = net.predict([caffImg], oversample=False)
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

net = initCaffe()
cap = initCv()
sns = initSnd()

counter = 0
last_snd = 3

while True:

    ret, img = readImg()
    if(ret == False):
        continue

    #cv2.imshow('camera', img)
    img = cvtImg(img)

    score0 = predict(img)
    print(score0)

    last_snd = playSound(score0, last_snd)

    if(handleKeyInput()):
        break

cap.release()
cv2.destroyAllWindows()
