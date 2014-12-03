#!/bin/sh

PYOPENCL_CTX=1
PYTHONPATH=../bumps:../periodictable:../sasview/build/lib.macosx-10.5-x86_64-2.7
export PYOPENCL_CTX PYTHONPATH

for dim in 1d100 2d32; do
    ./compare_many.py all 100 $dim 0 > $dim_poly_0.csv
    ./compare_many.py all 100 $dim 1e-5 > $dim_poly_1e-5.csv
    ./compare_many.py all 100 $dim 1e-3 > $dim_poly_1e-3.csv
    ./compare_many.py all 10000 $dim mono > $dim_mono.csv
done