import caffe
import os
import sys
import cv2
import numpy as np
import pygame
import datetime
import time
import errno
import picamera
from picamera.array import PiRGBArray

CAFFE_IMG_WIDTH = 64
CAFFE_IMG_HEIGHT = 64

CAMERA_WIDTH = 320
CAMERA_HEIGHT = 240

raw = None
cam = None

def initCv():
    camera = picamera.PiCamera()
    camera.resolution = (CAMERA_WIDTH, CAMERA_HEIGHT)
    camera.led = True
    camera.framerate = 32
    rawCap = PiRGBArray(camera, size=(CAMERA_WIDTH, CAMERA_HEIGHT))

    #warm up
    time.sleep(0.1)

    return camera, rawCap

def showImg(img):
    width = img.shape[1]
    height = img.shape[0]
    edge_len = int(height * 0.7)
    ori = (int((width - edge_len)/2), int((height-edge_len)/2))

    img_rect = img.copy()
    
    cv2.rectangle(img_rect, ori, (ori[0]+edge_len, ori[1]+edge_len), (255, 0, 0), 4)
    cv2.imshow('camera', img_rect)

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

cam, raw = initCv()

for frame in cam.capture_continuous(raw, format="bgr", use_video_port=True):

    img = frame.array

    #cv2.imshow('camera', img)
    showImg(img)

    if(handleKeyInput(img)):
        break
    raw.truncate(0)

cam.led = False
cv2.destroyAllWindows()
