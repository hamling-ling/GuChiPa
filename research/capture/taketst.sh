rm -rf tst

mkdir tst
mkdir tst/g
mkdir tst/c
mkdir tst/a
mkdir tst/z

python ../caffe_examples_guchipa/mv.py 1000 "gam/a/*.jpg" "tst/a/"
