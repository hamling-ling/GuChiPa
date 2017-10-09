'''
Title           :create_lmdb.py
Description     :This script divides the training images into 2 sets and stores them in lmdb databases for training and validation.
Author          :Adil Moujahid
Date Created    :20160619
Date Modified   :20160625
version         :0.2
usage           :python create_lmdb.py
python_version  :2.7.11
'''

import os
import glob
import random
import numpy as np

import cv2

import caffe
from caffe.proto import caffe_pb2
import lmdb
import re
import sys

#Size of images
IMAGE_WIDTH = 64
IMAGE_HEIGHT = 64

def transform_img(img, img_width=IMAGE_WIDTH, img_height=IMAGE_HEIGHT):

    #Histogram Equalization
    img[:, :, 0] = cv2.equalizeHist(img[:, :, 0])
    img[:, :, 1] = cv2.equalizeHist(img[:, :, 1])
    img[:, :, 2] = cv2.equalizeHist(img[:, :, 2])

    #Image Resizing
    img = cv2.resize(img, (img_width, img_height), interpolation = cv2.INTER_CUBIC)

    return img


def make_datum(img, label):
    #image is numpy.ndarray format. BGR instead of RGB
    return caffe_pb2.Datum(
        channels=3,
        width=IMAGE_WIDTH,
        height=IMAGE_HEIGHT,
        label=label,
        data=np.rollaxis(img, 2).tostring())


if(len(sys.argv) < 2):
    print("need srd and dst dir")
    exit(1)

src_dir = sys.argv[1]
lmdb_dir = sys.argv[2]

os.system('rm -rf  ' + lmdb_dir)

with open(src_dir + "/list_all.txt") as f:
    lines = f.readlines()

file_info_list = []
for line in lines:
    line = line.strip()
    m = re.search("\./(.+)\s(\d)", line)
    if m:
        file_info_list.append((m.group(1),m.group(2)))
#print(file_info_list)

#Shuffle train_data
random.shuffle(file_info_list)

print 'Creating train_lmdb'

in_db = lmdb.open(lmdb_dir, map_size=int(1e12))
in_idx = 0
in_txn = in_db.begin(write=True)
uncommitted_exist=False
for fn, lbl in file_info_list:
    full_fn = src_dir + "/all/" + fn

    img = cv2.imread(full_fn, cv2.IMREAD_COLOR)
    img = transform_img(img, img_width=IMAGE_WIDTH, img_height=IMAGE_HEIGHT)
    datum = make_datum(img, int(lbl))
    in_txn.put('{:0>5d}'.format(in_idx), datum.SerializeToString())
    uncommited_exist = True
    print '{:0>5d}'.format(in_idx) + ':' + fn

    if(in_idx % 1000 == 0):
        in_txn.commit()
        in_txn = in_db.begin(write=True)
        uncommited_exist = False
    in_idx = in_idx+1

if(uncommited_exist):
    in_txn.commit()

in_db.close()


print '\nFinished processing all images'
