import glob
import sys
import random
import subprocess
import os

if len(sys.argv) < 4:
    print("error. need two arguments")
    print('ex) mvrnd.py 3 "a/*.jpg" "b/"')
    exit(1)

num_file = int(sys.argv[1])
dir_src = sys.argv[2]
dir_dst = sys.argv[3]

files = glob.glob(dir_src)

if(len(files) < num_file):
    print("given file number({0}) exceeds actual file number({1})"
          .format(num_file, len(files)))
    exit(1)

if(os.path.exists(dir_dst) == False):
    print("{0} does not exist".format(dir_dst))
    exit(1)

if(os.path.isdir(dir_dst) == False):
    print("{0} is not a directory".format(dir_dst))
    exit(1)

selected_files = random.sample(files, num_file)
for f in selected_files:
    cmd = "mv {0} {1}".format(f, dir_dst)
    print(cmd)
    subprocess.call(cmd, shell=True)

print("finished")

