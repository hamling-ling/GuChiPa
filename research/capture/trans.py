import cv2
import glob
import os
import errno
import numpy as np

srcdir='scl'
dstdir='trn'

def make_sure_path_exists(path):
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise

def transImage(filename, trans):
    img = cv2.imread(filename,0)
    rows,cols = img.shape
    mat = np.float32([[1,0,cols*trans[0]],[0,1,rows*trans[1]]])
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
        trans_ys = [-0.2, 0.0,0.2]
        trans_xs = [-0.2, 0.0,0.2]
        for tr_x in trans_xs:
            for tr_y in trans_ys:
                img = transImage(file, (tr_x, tr_y))
                filename = file[len(srcdir+'/'+subdir+'/'):len(file)-4]
                filename = filename + '_tr'
                filename = filename + "{0:.1f}_{1:.1f}".format(tr_x,tr_y) + '.jpg'
                writeImage(img, subdir, filename)
    
process('g')
process('c')
process('a')
process('z')

