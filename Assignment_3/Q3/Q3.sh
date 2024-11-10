#!/bin/bash


for h in $(seq 7.00 0.02 8.00); do
  rm -r $h
  mkdir $h
  cp pt.scf.in $h
  cd $h
  sed "s/LCT/${h}/g" ../Q3_pt.scf.template > pt.scf.in
  pw.x < pt.scf.in > pt.out
  
  cd ..
done

