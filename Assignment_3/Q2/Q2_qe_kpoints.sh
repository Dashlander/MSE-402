#! /bin/bash

strings=("3 3 3 0 0 0" "3 3 3 1 1 1" "4 4 4 0 0 0" "4 4 4 1 1 1" "5 5 5 0 0 0" "5 5 5 1 1 1" "6 6 6 0 0 0" "6 6 6 1 1 1" "7 7 7 0 0 0" "7 7 7 1 1 1" "8 8 8 0 0 0" "8 8 8 1 1 1" "9 9 9 0 0 0" "9 9 9 1 1 1" "10 10 10 0 0 0" "10 10 10 1 1 1")

for h in "${strings[@]}"

do

echo "$h"

rm -r "$h"
mkdir "$h"

  cp Q2_pt.scf.template "$h"

  cd "$h"

   sed s/KPOINTS/"$h"/g < ../Q2_pt.scf.template > pt.scf.in
   
   pw.x < pt.scf.in > pt.out 

  cd ..

done

