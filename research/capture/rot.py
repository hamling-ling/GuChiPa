import cv2
import glob
import os
import errno
import sys
import numpy as np

srcdir='flp'
dstdir='rot'

def make_sure_path_exists(path):
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise

def rotImage(filename, degree):
    img = cv2.imread(filename,1)
    rows,cols,chs = img.shape
    M = cv2.getRotationMatrix2D((cols/2, rows/2), degree, 1.0)

    bg_img = np.zeros(img.shape, np.uint8)
    meancolor=np.mean(img,axis=(0,1))
    bg_img = bg_img + meancolor.astype(np.uint8)
    #print(meancolor)
    rot_img = cv2.warpAffine(img, M, (cols, rows), bg_img, borderMode=cv2.BORDER_TRANSPARENT)
    
    return rot_img

def writeImage(img, subdir, filename):
    make_sure_path_exists(dstdir)
    make_sure_path_exists(dstdir+'/'+subdir)
    fullname="{0}/{1}/{2}".format(dstdir,subdir,filename)

    cv2.imwrite(fullname, img)
    print("saved " + fullname)

def process(subdir) :
    files = glob.glob(srcdir+'/'+subdir+'/*.jpg')
    for file in files:
        degrees = [-30, 0, 30]
        for deg in degrees:
            img = rotImage(file, deg)
            filename = file[len(srcdir+'/'+subdir+'/'):len(file)-4]
            filename = filename + '_rot' + str(deg) + '.jpg'
            writeImage(img, subdir, filename)

if(len(sys.argv) <= 2):
    print("need src and dst dir")
    exit(1)

srcdir=sys.argv[1]
dstdir=sys.argv[2]

process('g')
process('c')
process('a')
process('z')

