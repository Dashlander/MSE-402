import re
import matplotlib.pyplot as plt

# Filepath for the output file (replace with your actual file path)
file_path = '/home/dashlander/Desktop/Sem7/CPD/Assignment_2/Q4/ising2d_40.log'

# Initialize lists to store kT/J values, energies, and magnetizations
kT_values = []
energies = []
magnetizations = []

# Regular expressions to capture kT/J, energy, and magnetization
kt_pattern = re.compile(r'kT/J:\s+([\d.]+)')
energy_pattern = re.compile(r'energy, magnetization\s+([-.\d]+)\s+([-.\d]+)')
final_pattern = re.compile(r'mean energy per spin:\s+([-.\d]+)\s+rms energy fluctuation')
final_mag_pattern = re.compile(r'mean magnetization per spin:\s+([-.\d]+)\s+rms magnetization fluctuation')

with open(file_path, 'r') as file:
    for line in file:
        # Find kT/J value
        kt_match = kt_pattern.search(line)
        if kt_match:
            kT_values.append(float(kt_match.group(1)))

        # Find energy and magnetization values
        energy_mag_match = energy_pattern.search(line)
        if energy_mag_match:
            energies.append(float(energy_mag_match.group(1)))
            magnetizations.append(float(energy_mag_match.group(2)))

        # Handle final mean energy per spin (if exists in another format)
        final_energy_match = final_pattern.search(line)
        final_mag_match = final_mag_pattern.search(line)
        if final_energy_match:
            energies[-1] = float(final_energy_match.group(1))
        if final_mag_match:
            magnetizations[-1] = float(final_mag_match.group(1))

# Plot energy vs kT/J
plt.figure(figsize=(10,5))
plt.subplot(1, 2, 1)
plt.plot(kT_values, energies, 'o-', label='Energy')
plt.xlabel('kT/J')
plt.ylabel('Energy')
plt.title('Energy vs kT/J')
plt.grid(True)

# Plot magnetization vs kT/J
plt.subplot(1, 2, 2)
plt.plot(kT_values, magnetizations, 'o-', label='Magnetization', color='orange')
plt.xlabel('kT/J')
plt.ylabel('Magnetization')
plt.title('Magnetization vs kT/J')
plt.grid(True)

plt.tight_layout()
plt.show()
