import cv2
import glob
import os
import errno
import numpy as np

srcdir='trn'
dstdir='cnt'

min_table = 50
max_table = 205
diff_table = max_table - min_table

LUT_HC = np.arange(256, dtype = 'uint8' )
LUT_LC = np.arange(256, dtype = 'uint8' )

for i in range(0, min_table):
    LUT_HC[i] = 0
for i in range(min_table, max_table):
    LUT_HC[i] = 255 * (i - min_table) / diff_table
for i in range(max_table, 255):
    LUT_HC[i] = 255

for i in range(256):
    LUT_LC[i] = min_table + i * (diff_table) / 255

def make_sure_path_exists(path):
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise

def contrastImage(filename, cont):
    img = cv2.imread(filename,0)
    if(cont == -1):
        return cv2.LUT(img, LUT_LC)
    if(cont == 1):
        return cv2.LUT(img, LUT_HC)
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
            img = contrastImage(file, cont)
            filename = file[len(srcdir+'/'+subdir+'/'):len(file)-4]
            filename = filename + '_ct'
            filename = filename + "{0}".format(cont) + '.jpg'
            writeImage(img, subdir, filename)

process('g')
process('c')
process('a')
process('z')

