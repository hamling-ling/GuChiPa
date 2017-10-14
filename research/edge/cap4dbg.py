import caffe
import os
import sys
import cv2
import numpy as np
import pygame
import datetime
import time
import errno

CAFFE_IMG_WIDTH = 64
CAFFE_IMG_HEIGHT = 64


def initCv():
    capture = cv2.VideoCapture(0)
    capture.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH,320);
    capture.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT,240);

    return capture

def cvtImg(img):
    #img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

    width = img.shape[1]
    height = img.shape[0]
    offset = (width-height)/2
    edge_len=height
    
    crop_img = img[0:edge_len, offset:offset+edge_len, :]

    cv2.imshow('camera', crop_img)
    
    scaled_img = cv2.resize(crop_img,(CAFFE_IMG_WIDTH,CAFFE_IMG_HEIGHT))
    #print("resized shape={0}".format(img.shape))
    scaled_img = np.reshape(scaled_img,(CAFFE_IMG_WIDTH,CAFFE_IMG_HEIGHT,3))

    return scaled_img

def readImg():
    ret,img = cap.read(0)
    if ret == False:
        print("read image failed")

    return ret, img

def make_sure_path_exists(path):
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise

def cmd2dir(cmd):
    if(cmd == 103):
        return 'g'
    elif(cmd == 99):
        return 'c'
    elif(cmd== 97):
        return 'a'
    elif(cmd== 122):
        return 'z'
    return 'x'

def still(cmd, image):
    supported_cmds = [103, 99, 97, 122]
    if (cmd in supported_cmds) == False:
        #print("not recognized:" + cmd)
        return

    now = datetime.datetime.now()
    file = now.strftime("%Y%m%d_%H%M%S") + ".jpg"
    dir = cmd2dir(cmd)
    make_sure_path_exists(dir)
    fullname = dir + '/' + file
    
    cv2.imwrite(fullname, image)
    print("saved " + fullname)


def handleKeyInput(img):
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
    else:
        still(key, img)
    return False

cap = initCv()

while True:

    ret, img = readImg()
    if(ret == False):
        continue

    #cv2.imshow('camera', img)
    img = cvtImg(img)

    if(handleKeyInput(img)):
        break

cap.release()
cv2.destroyAllWindows()
