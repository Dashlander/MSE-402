import numpy as np
import matplotlib.pyplot as plt
import os

directories = sorted([d for d in os.listdir() if os.path.isdir(d)])
print(directories)

x = []
for i in directories:
    td = f'/home/dashlander/Desktop/Sem7/CPD/Assignment_3/Q1/{i}'
    os.chdir(td)
    filename = 'pt.out'
    with open(filename, 'r') as file:
        for line in file:
            if line.startswith('!'):
                z = line.split()
                print(z)
                x.append(z[4])

k = [float(i)*13.6057039763 for i in x]
plt.plot(directories, k, 'o-')
plt.xlabel('Energy Cutoff(Ry)')
plt.ylabel('Ground State Energy(eV)')
plt.title('Ground State Variation with changing Energy values')
plt.grid(True)
plt.show()
print(x)