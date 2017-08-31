import cv2
import glob
import os
import errno

srcdir='crp'
dstdir='flp'

def make_sure_path_exists(path):
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise

def flipImage(filename, flip):
    img = cv2.imread(filename)
    if(flip):
        flip_img = cv2.flip(img, 1)
    else:
        flip_img = img
    return flip_img

def writeImage(img, subdir, filename):
    make_sure_path_exists(dstdir)
    make_sure_path_exists(dstdir+'/'+subdir)
    fullname="{0}/{1}/{2}".format(dstdir,subdir,filename)

    cv2.imwrite(fullname, img)
    print("saved " + fullname)

def process(subdir) :
    files = glob.glob(srcdir+'/'+subdir+'/*.jpg')
    for file in files:
        img = flipImage(file, False)
        filename = file[len(srcdir+'/'+subdir+'/'):len(file)-4]
        filename = filename + '_l.jpg'
        writeImage(img, subdir, filename)

        img = flipImage(file, True)
        filename = file[len(srcdir+'/'+subdir+'/'):len(file)-4]
        filename = filename + '_r.jpg'
        writeImage(img, subdir, filename)

process('g')
process('c')
process('a')
process('z')

