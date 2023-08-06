#!/bin/bash

SOFTWARE_FOLDER=".cuprocell"
CUPROCELL_ROOT=$HOME/$SOFTWARE_FOLDER
CUPROCELL_URL="https://github.com/ericniso/cuda-pro-cell.git"
CUPROCELL="cuprocell"
GPU_ARCH="sm_35"

if [ -d $CUPROCELL_ROOT ]; then
    rm -rf $CUPROCELL_ROOT
fi

echo "Creating $CUPROCELL_ROOT directory..."

mkdir -p $CUPROCELL_ROOT

echo "Entering $CUPROCELL_ROOT directory..."

cd $CUPROCELL_ROOT

git clone $CUPROCELL_URL $CUPROCELL

cd $CUPROCELL

mkdir build && cd build

cmake -DCMAKE_CUDA_FLAGS="-arch=$GPU_ARCH" ..

make
