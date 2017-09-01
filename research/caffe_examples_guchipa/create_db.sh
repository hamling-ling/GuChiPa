rm -rf train_lmdb
rm -rf test_lmdb

echo creating train_leveldb
$CAFFE_ROOT/build/tools/convert_imageset data/nnsrc/all/ data/nnsrc/list_all.txt train_lmdb --backend lmdb --shuffle --resize_height 28 --resize_width 28 --gray

echo creating test_leveldb
$CAFFE_ROOT/build/tools/convert_imageset data/nntst/all/ data/nntst/list_all.txt test_lmdb --backend lmdb --resize_height 28 --resize_width 28 --gray
