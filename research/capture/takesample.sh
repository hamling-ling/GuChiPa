NUM=$1
SRC=$2
DST=$3

rm -rf $1

mkdir $DST
mkdir $DST/g
mkdir $DST/c
mkdir $DST/a
mkdir $DST/z

python ../caffe_examples_guchipa/mvrnd.py "$NUM" "$SRC/g/*.jpg" "$DST/g/"
python ../caffe_examples_guchipa/mvrnd.py "$NUM" "$SRC/c/*.jpg" "$DST/c/"
python ../caffe_examples_guchipa/mvrnd.py "$NUM" "$SRC/a/*.jpg" "$DST/a/"
python ../caffe_examples_guchipa/mvrnd.py "$NUM" "$SRC/z/*.jpg" "$DST/z/"
