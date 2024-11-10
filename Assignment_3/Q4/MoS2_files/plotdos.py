import matplotlib.pyplot as plt
import numpy as np

# Load data, skipping the first line (header)
data = np.loadtxt('/home/dashlander/Desktop/Sem7/CPD/Assignment_3/Q4/MoS2_files/MoS2_dos.dat', skiprows=1)

# Extract the first two columns
x = data[:, 0]  # E (eV)
y = data[:, 1]  # dos(E)

# Create the plot
plt.figure(figsize=(8, 6))
plt.plot(x, y, color='k', linewidth=1.5)  # Plot with black line
plt.title("Density of States (DOS) vs Energy")
plt.xlabel("Energy (eV)")
plt.ylabel("DOS (arb. units)")
plt.xlim(min(x), max(x))  # Set x-axis limits
plt.grid()  # Add grid for better readability
plt.tight_layout()  # Adjust layout to prevent clipping

# Show the plot
plt.show()
