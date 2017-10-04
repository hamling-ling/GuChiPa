rm -rf lmdb

$CAFFE_ROOT/build/tools/convert_imageset ./ list.txt lmdb --backend lmdb --shuffle --resize_height 64 --resize_width 64

