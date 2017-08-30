import cv2
import glob
import os
import errno
import numpy as np

srcdir='gau'
dstdir='spn'

def make_sure_path_exists(path):
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise

def saltNoiseImage(filename, param):
    img = cv2.imread(filename)
    if(param == 0):
        return img
    
    row,col,ch = img.shape
    s_vs_p = 0.5
    amount = 0.004
    sp_img = img.copy()

    # 塩モード
    if(param == 1):
        num_salt = np.ceil(amount * img.size * s_vs_p)
        coords = [np.random.randint(0, i-1 , int(num_salt)) for i in img.shape]
        sp_img[coords[:-1]] = (255,255,255)
        return sp_img
    elif(param == -1):
        # 胡椒モード
        num_pepper = np.ceil(amount* img.size * (1. - s_vs_p))
        coords = [np.random.randint(0, i-1 , int(num_pepper)) for i in img.shape]
        sp_img[coords[:-1]] = (0,0,0)
        return sp_img
    else:
        return img

def writeImage(img, subdir, filename):
    make_sure_path_exists(dstdir)
    make_sure_path_exists(dstdir+'/'+subdir)
    fullname="{0}/{1}/{2}".format(dstdir,subdir,filename)

    cv2.imwrite(fullname, img)
    print("saved " + fullname)

def process(subdir) :
    files = glob.glob(srcdir+'/'+subdir+'/*.png')
    for file in files:
        params = [-1, 0, 1]
        for p in params:
            img = saltNoiseImage(file, p)
            filename = file[len(srcdir+'/'+subdir+'/'):len(file)-4]
            filename = filename + '_sp'
            filename = filename + "{0}".format(int(p)) + '.png'
            writeImage(img, subdir, filename)

process('g')
process('c')
process('a')

