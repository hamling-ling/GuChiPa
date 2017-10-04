import caffe
import os
import sys
import glob

CAFFE_ROOT = os.getenv("CAFFE_ROOT")
MODEL_FILE = CAFFE_ROOT + '/examples/lelenet_bg/lenet.prototxt'
PRETRAINED = CAFFE_ROOT + '/examples/lelenet_bg/lenet_iter_10000.caffemodel'

def scoreToCharLabel(score):
    charLbl = 'z'
    if(score[0] > 0.9):
        charLbl = 'g'
    elif(score[1] > 0.9):
        charLbl = 'c'
    elif(score[2] > 0.9):
        charLbl = 'a'
    else:
        charLbl = 'z'
    return charLbl

def enumFiles(srcdir, subdir) :
    jpgs = glob.glob(srcdir+'/'+subdir+'/*.jpg')
    pngs = glob.glob(srcdir+'/'+subdir+'/*.png')
    all = pngs
    all.extend(jpgs)
    return all

def process(srcdir, subdir) :
    files = enumFiles(srcdir, subdir)
    for file in files:
        image = caffe.io.load_image(file, color=True)
        #print(image.shape)
        score = net.predict([image], oversample=False)
        #print score
        charLbl = scoreToCharLabel(score[0])
        if charLbl == subdir :
            result="    "
        else :
            result = "[NG]"
        print("{0} {1}".format(result, file))
        
if(len(sys.argv) < 2):
    print("need image file")
    exit(1)

srcdir = sys.argv[1]

net = caffe.Classifier(MODEL_FILE, PRETRAINED, image_dims=(64,64), raw_scale=255)
caffe.set_mode_cpu()
#caffe.set_mode_gpu()

process(srcdir, "g")
process(srcdir, "c")
process(srcdir, "a")
process(srcdir, "z")
