import cv2
import glob
import os
import errno
import numpy as np
import sys

srcdir='scl'
dstdir='trn'

def make_sure_path_exists(path):
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise

def transImage(filename, trans):
    img = cv2.imread(filename,1)
    rows,cols,chs = img.shape
    mat = np.float32([[1,0,rows*trans[0]],[0,1,rows*trans[1]]])
    rot_img = cv2.warpAffine(img, mat, (cols, rows))
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
        trans_ys = [-0.1, 0.0,0.1]
        trans_xs = [-0.1, 0.0,0.1]
        for tr_x in trans_xs:
            for tr_y in trans_ys:
                
                if tr_x == 0.0 and tr_y != 0.0:
                    #skip horizontal trans to reduce file num
                    continue
                if tr_x != 0.0 and tr_y == 0.0:
                    #skip vertical trans to reduce file num
                    continue
                img = transImage(file, (tr_x, tr_y))
                filename = file[len(srcdir+'/'+subdir+'/'):len(file)-4]
                filename = filename + '_tr'
                filename = filename + "{0:.1f}_{1:.1f}".format(tr_x,tr_y) + '.jpg'
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

