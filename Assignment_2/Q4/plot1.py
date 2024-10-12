import numpy as np
import matplotlib.pyplot as plt

# Function to read the data from the file and return kT/J values and corresponding fluctuation values
def read_data(file_path):
    with open(file_path, 'r') as file:
        data = file.read().split()

    # Convert data from strings to floats
    data = list(map(float, data))

    # kT/J values are at even indices, fluctuation values at odd indices
    kT_values = data[0::2]
    fluct_values = data[1::2]
    
    return np.array(kT_values), np.array(fluct_values)

# Filepaths
energy_file = 'eflucvst.1'
magnetization_file = 'mflucvst.1'

# Read energy fluctuation and magnetization fluctuation data
kT_energy, energy_fluct = read_data(energy_file)
kT_magnetization, magnetization_fluct = read_data(magnetization_file)

# Plot energy fluctuation vs kT/J
plt.figure(figsize=(12, 6))

plt.subplot(1, 2, 1)
plt.plot(kT_energy, energy_fluct, 'b-o', label='Energy Fluctuation')
plt.xlabel('kT/J')
plt.ylabel('Energy Fluctuation')
plt.title('Energy Fluctuation vs kT/J')
plt.grid(True)  # Reverse x-axis for descending kT/J values

# Plot magnetization fluctuation vs kT/J
plt.subplot(1, 2, 2)
plt.plot(kT_magnetization, magnetization_fluct, 'r-o', label='Magnetization Fluctuation')
plt.xlabel('kT/J')
plt.ylabel('Magnetization Fluctuation')
plt.title('Magnetization Fluctuation vs kT/J')
plt.grid(True)  # Reverse x-axis for descending kT/J values

# Adjust layout and display the plot
plt.tight_layout()
plt.show()
