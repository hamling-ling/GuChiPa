import cv2
import glob
import os
import errno

srcdir='raw'
dstdir='crp'

width=640
height=480
edge_len=int(height*0.8-10)
crop_ori=(int((width-edge_len)/2),int((height-edge_len)/2))


def make_sure_path_exists(path):
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise

def cropImage(filename):
    img = cv2.imread(filename)
    crop_img = img[crop_ori[1]:crop_ori[1]+edge_len, crop_ori[0]:crop_ori[0]+edge_len]
    #cv2.imshow("cropped", crop_img)
    #cv2.waitKey(0)
    return crop_img

def writeImage(img, subdir, filename):
    make_sure_path_exists(dstdir)
    make_sure_path_exists(dstdir+'/'+subdir)
    fullname="{0}/{1}/{2}".format(dstdir,subdir,filename)
    #print("{0}/{1}/{2}".format(dstdir,subdir,filename))
    #fullname = dir + '/' + subdir + '/' + filename

    cv2.imwrite(fullname, img)
    print("saved " + fullname)

def processCrop(subdir) :
    files = glob.glob(srcdir+'/'+subdir+'/*.png')
    for file in files:
        img = cropImage(file)
        filename = file[len(srcdir+'/'+subdir+'/'):len(file)]
        writeImage(img, subdir, filename)

processCrop('g')
processCrop('c')
processCrop('a')

