import cv2
import glob
import os
import errno
import numpy as np
import sys

srcdir='cnt'
dstdir='gam'

min_table = 50
max_table = 205
diff_table = max_table - min_table

LUT_G1 = np.arange(256, dtype = 'uint8' )
LUT_G2 = np.arange(256, dtype = 'uint8' )

gamma1 = 0.75
gamma2 = 1.5
for i in range(256):
    LUT_G1[i] = 255 * pow(float(i) / 255, 1.0 / gamma1)
    LUT_G2[i] = 255 * pow(float(i) / 255, 1.0 / gamma2)

def make_sure_path_exists(path):
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise

def gammaImage(filename, cont):
    img = cv2.imread(filename,0)
    if(cont == -1):
        return cv2.LUT(img, LUT_G1)
    if(cont == 1):
        return cv2.LUT(img, LUT_G2)
    return img

def writeImage(img, subdir, filename):
    make_sure_path_exists(dstdir)
    make_sure_path_exists(dstdir+'/'+subdir)
    fullname="{0}/{1}/{2}".format(dstdir,subdir,filename)

    cv2.imwrite(fullname, img)
    print("saved " + fullname)

def process(subdir) :
    files = glob.glob(srcdir+'/'+subdir+'/*.jpg')
    for file in files:
        contrasts= [-1, 0, 1]
        for cont in contrasts:
            img = gammaImage(file, cont)
            filename = file[len(srcdir+'/'+subdir+'/'):len(file)-4]
            filename = filename + '_gm'
            filename = filename + "{0}".format(cont) + '.jpg'
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

