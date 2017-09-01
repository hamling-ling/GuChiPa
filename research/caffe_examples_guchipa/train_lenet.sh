#!/usr/bin/env sh
set -e

./build/tools/caffe train --solver=examples/guchipa/lenet_solver.prototxt $@
