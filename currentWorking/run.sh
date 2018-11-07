#!/bin/bash

FILES="$@"
for program in $FILES
do
    for rate in $(seq 0.1 0.1 1.0)
    do
        python $program $rate
    done
done
