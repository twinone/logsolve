#!/bin/bash

testdir="test"
names="$(ls $testdir)"


for name in $names; do
  fname=$(echo $name|cut -d- -f1)
  xy=$(echo $name|cut -d- -f2|cut -d. -f1)
  x=$(echo $xy | cut -dx -f1)
  y=$(echo $xy | cut -dx -f2)

  ./test_gridsize.py $testdir/$name $x $y
done
