rm -rf train_leveldb

../../build/tools/convert_imageset data/nnsrc/all/ data/nnsrc/list_all.txt train_leveldb 1 -backend leveldb 28 28

