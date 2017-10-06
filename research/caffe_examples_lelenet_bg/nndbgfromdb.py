import sys
import os
import caffe
import numpy as np
from PIL import Image as image
import lmdb
import cv2
import errno

def make_sure_path_exists(path):
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise

def readImg(key, value):
    datum = caffe.proto.caffe_pb2.Datum()
    datum.ParseFromString(value)
    lbl = int(datum.label)

    img = caffe.io.datum_to_array(datum)
    img = img.astype(np.uint8)
    return img, lbl

def writeImg(img, index, label, dstdir):
    data=np.asarray([img])
    a=data[0][0]

    fn = "{0}/{1}/{2}.png".format(dstdir,label,index)
    img=np.transpose(img, (1,2,0))
    cv2.imwrite(fn, img)
    print("{0} saved".format(fn))


tbl_int2label = np.array(['g','c','a','z'])
caffe_root = os.getenv("CAFFE_ROOT")

db_path = caffe_root + '/examples/lelenet_bg/train_lmdb'
if(len(sys.argv) < 3):
    print("need [db file] [file num] [out dir]")
    exit(1)

db_path = sys.argv[1]
img_num = int(sys.argv[2])
out_dir = sys.argv[3]

make_sure_path_exists(out_dir)
for i in range(len(tbl_int2label)):
    make_sure_path_exists(out_dir + '/' + tbl_int2label[i])

lmdb_env = lmdb.open(db_path)
lmdb_txn = lmdb_env.begin()
lmdb_cursor = lmdb_txn.cursor()
count = 0

for key, value in lmdb_cursor:
    if count >= img_num:
	break
    img, lbl=readImg(key, value)
    lbl_str=tbl_int2label[lbl]
    writeImg(img, count, lbl_str, out_dir)
    count = count+1

