#!/usr/bin/env sh
set -e

./build/tools/caffe train --solver=examples/lelenet/lenet_solver.prototxt $@
