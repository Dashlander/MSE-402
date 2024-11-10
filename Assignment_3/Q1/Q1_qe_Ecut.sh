#!/bin/bash


for h in $(seq 10 5 40); do
  rm -r $h
  mkdir $h
  cp pt.scf.in $h
  cd $h
  sed "s/ECUTOFF/${h}/g" ../Q1_pt.scf.template > pt.scf.in
  pw.x < pt.scf.in > pt.out
  
  cd ..
done

