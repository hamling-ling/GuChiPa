python ../code/create_lmdb.py data/nntst test_lmdb
python ../code/create_lmdb.py data/nnsrc train_lmdb

$CAFFE_ROOT/build/tools/compute_image_mean -backend=lmdb train_lmdb mean.binaryproto
