import cv2
import glob
import os
import errno
import numpy as np

srcdir='gam'
dstdir='gau'

def make_sure_path_exists(path):
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise

def gaussNoiseImage(filename, apply):
    img = cv2.imread(filename)
    if(apply == False):
        return img
    row,col,ch= img.shape
    mean = 0
    sigma = 15
    gauss = np.random.normal(mean,sigma,(row,col,ch))
    gauss = gauss.reshape(row,col,ch)
    gauss_img = img + gauss
    return gauss_img

def writeImage(img, subdir, filename):
    make_sure_path_exists(dstdir)
    make_sure_path_exists(dstdir+'/'+subdir)
    fullname="{0}/{1}/{2}".format(dstdir,subdir,filename)

    cv2.imwrite(fullname, img)
    print("saved " + fullname)

def process(subdir) :
    files = glob.glob(srcdir+'/'+subdir+'/*.jpg')
    for file in files:
        params = [False, True]
        for p in params:
            img = gaussNoiseImage(file, p)
            filename = file[len(srcdir+'/'+subdir+'/'):len(file)-4]
            filename = filename + '_gs'
            filename = filename + "{0}".format(int(p)) + '.jpg'
            writeImage(img, subdir, filename)

process('g')
process('c')
process('a')
process('z')

