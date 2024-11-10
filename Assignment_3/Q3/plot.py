import numpy as np
import matplotlib.pyplot as plt
import os

directories = sorted([d for d in os.listdir() if os.path.isdir(d)], key=lambda x: list(map(float, x.split())))
e0 = []
for i in directories:
    print(i)
    td = f'/home/dashlander/Desktop/Sem7/CPD/Assignment_3/Q3/{i}'
    os.chdir(td)
    filename = 'pt.out'
    with open(filename, 'r') as file:
        for line in file:
            if line.startswith('!'):
                z = line.split()
                e0.append(z[4])
                print(z[4])

os.chdir('/home/dashlander/Desktop/Sem7/CPD/Assignment_3/Q3/')

eV0 = [float(i)*13.6057039763 for i in e0]
d0 = [float(i)**3 for i in directories]

plt.plot(d0, eV0, 'o-')
plt.xlabel('Volume(in au)')
plt.ylabel('Total Energy(eV)')
plt.title('Energy Variation with Volume')
plt.grid(True)
plt.legend()
plt.show()

import csv

data_nonshifted = list(zip(directories, d0, eV0))

csv_filename = "volvse02.csv"
with open(csv_filename, mode='w', newline='') as csv_file:
    writer = csv.writer(csv_file)
    # Write headers
    writer.writerow(["Volume", "Energy (eV)"])

    # Write non-shifted data
    for directory, k_points, energy in data_nonshifted:
        writer.writerow([k_points, energy])