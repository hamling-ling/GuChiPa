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
import random

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


def initCv():
    camera = picamera.PiCamera()
    camera.resolution = (CAMERA_WIDTH, CAMERA_HEIGHT)
    camera.led = True
    camera.framerate = 32
    camera.hflip = True
    rawCap = PiRGBArray(camera, size=(CAMERA_WIDTH, CAMERA_HEIGHT))

    #warm up
    time.sleep(0.1)

    return camera, rawCap

pygame.init()
screen = pygame.display.set_mode((800, 450))

cam, raw = initCv()
done = False

kEnemyStateIdle = 0
kEnemyStateInMotion = 1
kEnemyStateGuchipa = 2
kEnemyStatePlayerWin = 3
kEnemyStatePlayerLose = 4

kChallengeResultNoCount = -2
kChallengeResultPlayerLose = -1
kChallengeResultDraw = 0
kChallengeResultPlayerWin = 1

pygame.font.init()
myfont = pygame.font.SysFont('Comic Sans MS', 30)
txtimg_tapme = myfont.render('Tap Me!', False, (255, 0, 0))
txtimg_youlose = myfont.render('You Lost', False, (255, 0, 0))
txtimg_youwin = myfont.render('You Win!', False, (255,0, 0))
txtimg_none = myfont.render('', False, (0,0,0))

class Enemy():
    def __init__(self):
        self.img_halt = pygame.image.load("guchipa_resources/halt.jpg").convert()
        self.img_inmotion = pygame.image.load("guchipa_resources/inmotion.jpg").convert()
        self.img_playerwin = pygame.image.load("guchipa_resources/playerwin.jpg").convert()
        self.img_playerlose = pygame.image.load("guchipa_resources/playerlose.jpg").convert()
        
        self.img_g = pygame.image.load("guchipa_resources/g.jpg").convert()
        self.img_c = pygame.image.load("guchipa_resources/c.jpg").convert()
        self.img_a = pygame.image.load("guchipa_resources/a.jpg").convert()
        self.img_results = []
        self.state = kEnemyStateIdle
        self.guchipa = 0
        self.img_guchipa = [self.img_g, self.img_c, self.img_a]

        pygame.mixer.init()
        snd_g = pygame.mixer.Sound('snd/g.wav')
        snd_c = pygame.mixer.Sound('snd/c.wav')
        snd_a = pygame.mixer.Sound('snd/a.wav')
        self.sounds = [snd_g, snd_c, snd_a]
        self.last_gouchipa = 3

        self.snd_draw = pygame.mixer.Sound('snd/draw.wav')
        self.snd_playerwin = pygame.mixer.Sound('snd/playerwin.wav')
        self.snd_playerlose = pygame.mixer.Sound('snd/playerlose.wav')
        self.snd_start = pygame.mixer.Sound('snd/start.wav')
        
    def getImage(self):
        if(self.state == kEnemyStateGuchipa):
            return self.img_guchipa[self.result]
        if(self.state == kEnemyStateIdle):
            return self.img_halt
        if(self.state == kEnemyStatePlayerWin):
            return self.img_playerwin
        if(self.state == kEnemyStatePlayerLose):
            return self.img_playerlose
        return self.img_inmotion

    def start(self, is_restart):        
        self.state = 1
        self.starttime = time.time()
        self.last_guchipa = 3
        if(is_restart):
            self.snd_draw.play()
        else:
            self.snd_start.play()
        
    def tick(self):
        if(self.state == 1):
            delta=time.time() - self.starttime
            if(2 < delta):
                self.state = 2
                self.starttime = time.time()
                self.result = random.randint(0,2)
                print("enepy:{0}".format(self.result))
        return self.state

    def challenge(self, guchipa):
        print("challenge({0})".format(guchipa))
        if(guchipa < 0 or 2 < guchipa):
            return kChallengeResultNoCount
        self.playGuchipaSound(guchipa)
        
        ret = kChallengeResultPlayerWin
        if(self.result == guchipa):
            ret = kChallengeResultDraw
        if(self.result == 0):# enemy=g
            if(guchipa == 1):# player=c
                ret = kChallengeResultPlayerLose
        elif(self.result == 1):# enemy=c
            if(guchipa == 2):# player=a
                ret = kChallengeResultPlayerLose
        else: # enemy=a
            if(guchipa == 0):# player=g
                ret = kChallengeResultPlayerLose

        if(ret == kChallengeResultPlayerWin):
            self.state = kEnemyStatePlayerWin
            self.last_guchipa=3
            print("back to idle state")
            self.snd_playerwin.play()
        elif(ret == kChallengeResultPlayerLose):
            self.state = kEnemyStatePlayerLose
            self.last_guchipa=3
            print("back to idle state")
            self.snd_playerlose.play()
        elif(ret == kChallengeResultDraw):
            self.start(True)
        else:
            print("bug!")
        return ret

    def playGuchipaSound(self, guchipa):
        if(guchipa < 0 or 3 < guchipa):
            print("unexpected guchipa value error!")
            return
        if(guchipa != 3 and self.last_guchipa != guchipa):
            self.sounds[guchipa].play()
            self.last_guchipa = guchipa

class Detector():
    def __init__(self):
        mean_blob = caffe_pb2.BlobProto()
        mean_array = None
        with open(MEAN_FILE) as f:
            mean_blob.ParseFromString(f.read())
            mean_array = np.asarray(mean_blob.data, dtype=np.float32).reshape(
                (mean_blob.channels, mean_blob.height, mean_blob.width))

            net = caffe.Net(MODEL_FILE, PRETRAINED,caffe.TEST)
            caffe.set_mode_cpu()

            #Define image transformers
            transformer = caffe.io.Transformer({'data': net.blobs['data'].data.shape})
            transformer.set_mean('data', mean_array)
            transformer.set_transpose('data', (2,0,1))
        self.net = net
        self.transformer = transformer

    def predict(self, img):
        # warok around
        img_path = '/tmp/tmp.jpg'
        cv2.imwrite(img_path, img)
        img = cv2.imread(img_path, cv2.IMREAD_COLOR)
        img = self.transform_img(img, img_width=CAFFE_IMAGE_WIDTH, img_height=CAFFE_IMAGE_HEIGHT)

        self.net.blobs['data'].data[...] = self.transformer.preprocess('data', img)
        out = self.net.forward()
        score = out['prob']
    
        return score[0]

    def cropImg(self, img):
        width = img.shape[1]
        height = img.shape[0]
        offset = (width-height)/2
        edge_len=height

        crop_img = img[0:edge_len, offset:offset+edge_len, :]
    
        return crop_img

    def transform_img(self, img, img_width=CAFFE_IMAGE_WIDTH, img_height=CAFFE_IMAGE_HEIGHT):    
        #Histogram Equalization
        img[:, :, 0] = cv2.equalizeHist(img[:, :, 0])
        img[:, :, 1] = cv2.equalizeHist(img[:, :, 1])
        img[:, :, 2] = cv2.equalizeHist(img[:, :, 2])

        #Image Resizing
        img = cv2.resize(img, (img_width, img_height), interpolation = cv2.INTER_CUBIC)

        return img

    def translateScore(self, score):
        index = 0
        
        if(score[0] > 0.9):
            index = 0
        elif(score[1] > 0.9):
            index = 1
        elif(score[2] > 0.9):
            index = 2
        else:
            index = 3
        return index

detector = Detector()
enemy = Enemy()

player_state_txt = None
for frame in cam.capture_continuous(raw, format="bgr", use_video_port=True):

    img = frame.array
    img = detector.cropImg(img)

    enemy.tick()

    if(enemy.state == 2):
        score = detector.predict(img)
        guchipa = detector.translateScore(score)
        #print("{0}:{1}".format(guchipa, score))
        result = enemy.challenge(guchipa)
        if(result == kChallengeResultPlayerWin):
            player_state_txt = txtimg_youwin
            print("player win")
        elif(result == kChallengeResultPlayerLose):
            player_state_txt = txtimg_youlose
            print("player lose")
    elif(enemy.state == 1):
        player_state_txt = None
    
    #bg_img = bg_img_halt
    bg_img = enemy.getImage()
    
    screen.blit(bg_img, (400,0))
    
    rgb_img=img[:,:,::-1]
    pyg_shape = rgb_img.shape[1::-1]
    pyg_img = pygame.image.frombuffer(rgb_img.tostring(), pyg_shape, 'RGB')
    screen.blit(pyg_img, (0, 200))

    screen.blit(txtimg_tapme, (550, 100))

    if(player_state_txt != None):
        screen.blit(player_state_txt, (0, 200))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
            break
        elif event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            #print(pos)
            enemy.start(False)
    if(done):
        break

    pygame.display.flip()

    raw.truncate(0)

cam.led = False

