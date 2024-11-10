import numpy as np
import matplotlib.pyplot as plt
import os

directories = sorted([d for d in os.listdir() if os.path.isdir(d)], key=lambda x: list(map(int, x.split())))

list_0 = [d for d in directories if d.endswith('0 0 0')]
print(list_0)
list_1 = [d for d in directories if d.endswith('1 1 1')]
print(list_1)

# For non shifted
nk0 = []
e0 = []
for i in list_0:
    print(i)
    td = f'/home/dashlander/Desktop/Sem7/CPD/Assignment_3/Q2/{i}'
    os.chdir(td)
    filename = 'pt.out'
    with open(filename, 'r') as file:
        for line in file:
            if line.startswith('!'):
                z = line.split()
                e0.append(z[4])
                print(z[4])
            if "number of k points=" in line:
                w = line.split()
                nk0.append(w[4])
                print(w[4])

# For shifted
nk1 = []
e1 = []
for i in list_1:
    print(i)
    td = f'/home/dashlander/Desktop/Sem7/CPD/Assignment_3/Q2/{i}'
    os.chdir(td)
    filename = 'pt.out'
    with open(filename, 'r') as file:
        for line in file:
            if line.startswith('!'):
                z = line.split()
                e1.append(z[4])
                print(z[4])
            if "number of k points=" in line:
                w = line.split()
                nk1.append(w[4])
                print(w[4])

eV0 = [float(i)*13.6057039763 for i in e0]
eV1 = [float(i)*13.6057039763 for i in e1]
kn0 = [float(i) for i in nk0]
kn1 = [float(i) for i in nk1]

plt.plot(kn0, eV0, 'o-', label='nonshifted')
plt.plot(kn1, eV1, 'o-', label='shifted')
plt.xlabel('Number of unique K-Points after symmtery operations')
plt.ylabel('Total Energy(eV)')
plt.title('Energy Variation with Unique K points')
plt.grid(True)
plt.legend()
plt.show()

import csv

# Prepare data for CSV
# First, combine directory names, nk0, eV0 for non-shifted, and nk1, eV1 for shifted into rows
data_nonshifted = list(zip(list_0, kn0, eV0))
data_shifted = list(zip(list_1, kn1, eV1))

# Write data to CSV
csv_filename = "energy_kpoints_data.csv"
with open(csv_filename, mode='w', newline='') as csv_file:
    writer = csv.writer(csv_file)
    # Write headers
    writer.writerow(["Directory", "Unique K Points", "Energy (eV)", "Shifted"])

    # Write non-shifted data
    for directory, k_points, energy in data_nonshifted:
        writer.writerow([directory, k_points, energy, "nonshifted"])

    # Write shifted data
    for directory, k_points, energy in data_shifted:
        writer.writerow([directory, k_points, energy, "shifted"])

print(f"Data successfully written to {csv_filename}")