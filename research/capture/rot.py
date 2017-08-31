import cv2
import glob
import os
import errno

srcdir='flp'
dstdir='rot'

def make_sure_path_exists(path):
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise

def rotImage(filename, degree):
    img = cv2.imread(filename,0)
    rows,cols = img.shape
    M = cv2.getRotationMatrix2D((cols/2, rows/2), degree, 1.0)
    rot_img = cv2.warpAffine(img, M, (cols, rows))
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

process('g')
process('c')
process('a')
process('z')

