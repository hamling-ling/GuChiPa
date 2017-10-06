import caffe
import os
import sys
import glob
import numpy as np

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

def transform(img):
    img=(img*255).astype(np.uint8)
    img=np.rollaxis(img,2)
    s0=img[0,:,:]
    s1=img[1,:,:]
    s2=img[2,:,:]
    transformed=np.array([s2,s1,s0])
    return transformed

def process(srcdir, subdir) :
    files = enumFiles(srcdir, subdir)
    for file in files:
        image = caffe.io.load_image(file, color=True)
        image = transform(image)
        print(image.shape)
        #score = net.predict([image], oversample=False)
        net.blobs['data'].data[...] = [image]
        result = net.forward()
        score = result["prob"]
        print score
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

net = caffe.Classifier(
    MODEL_FILE,
    PRETRAINED,
    #image_dims=(3,64,64),
    #raw_scale=255,
    #channel_swap=(0,0,0)
)
caffe.set_mode_cpu()
#caffe.set_mode_gpu()
for layer_name, blob in net.blobs.iteritems():
        print layer_name + '\t' + str(blob.data.shape)

process(srcdir, "g")
process(srcdir, "c")
process(srcdir, "a")
process(srcdir, "z")
