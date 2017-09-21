import cv2
import os
import sys
import errno
import numpy as np

data_size = 28*28+1

def make_sure_path_exists(path):
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise

def extract_png(file, bin_idx, outpath):
    img = np.fromfile(f, dtype=np.dtype('uint8'), count=28*28)
    img = img.reshape(28,28)

    lbl = np.fromfile(f, dtype=np.dtype('uint8'), count=1)
    fn = "{0}.png".format(bin_idx)
    cv2.imwrite(outpath + '/' + fn, img)

    return lbl[0], fn

if(len(sys.argv) < 2):
    print("need bin file and out dir")
    exit(1)

bin_file_name = sys.argv[1]
out_dir_name = sys.argv[2]
if(out_dir_name[-1]=='/'):
    out_dir_name = out_dir_name[:-1]

txt_file_name = out_dir_name + '_images.txt'
bin_file_size = os.path.getsize(bin_file_name)

if(bin_file_size % (data_size) != 0):
    print("invalid file size of {0} : {1}".format(bin_file_name, bin_file_size))
    exit(1)

make_sure_path_exists(out_dir_name)
img_num = bin_file_size / data_size
f = open(bin_file_name, "rb")
ftxt = open(txt_file_name, "w")

for i in range(0,img_num):
    lbl, fn_png = extract_png(f, i, out_dir_name)
    line = "{0} {1}\n".format(fn_png, lbl)
    ftxt.write(line)
    print(line.strip())

f.close()
ftxt.close()

print("files written under {0}".format(out_dir_name))
print("label file created {0}".format(txt_file_name))
