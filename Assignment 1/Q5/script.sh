#!/bin/bash

cd "/home/dashlander/Desktop/Sem7/CPD/Assignment 1/Q5/Mem1/" || { echo "Failed to enter first directory"; exit 1; }
mpiexec -np 8 lmp_mpi -in input_nvt_CO2.in
wait

cd "/home/dashlander/Desktop/Sem7/CPD/Assignment 1/Q5/Mem2/" || { echo "Failed to enter Second directory"; exit 1; }
mpiexec -np 8 lmp_mpi -in input_nvt_CO2.in
wait

cd "/home/dashlander/Desktop/Sem7/CPD/Assignment 1/Q5/Mem3/" || { echo "Failed to enter Third directory"; exit 1; }
mpiexec -np 8 lmp_mpi -in input_nvt_CO2.in
wait
