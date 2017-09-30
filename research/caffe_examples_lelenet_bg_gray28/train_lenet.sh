#!/usr/bin/env sh
set -e

./build/tools/caffe train --solver=examples/lelenet_bg_gray28/lenet_solver.prototxt $@ 2>&1 | tee examples/lelenet_bg_gray28/train.log

