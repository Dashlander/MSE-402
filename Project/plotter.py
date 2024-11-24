import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter

# Read the data from a file (replace 'data.txt' with your actual filename)
filename = '/home/dashlander/Desktop/Sem7/CPD/Project/md21.log'

# Load the data assuming it's space-separated
data = np.loadtxt(filename)

# Select the columns to plot (e.g., first column against second column)
x = data[:, 0]  # First column (index 0)
y = data[:, 1]  # Second column (index 1)


# Moving average function
def moving_average(data, window_size):
    return np.convolve(data, np.ones(window_size)/window_size, mode='valid')

y_smooth = savgol_filter(y, 25, 3)

plt.plot(x, y_smooth, 'm-')
#plt.plot(x, y, 'r-')
plt.xlabel('Time')
plt.ylabel('Potential Energy (kCal/mol)')
plt.title('Potential Energy vs Time')
plt.grid()
plt.show()

z = data[:, 2]
z_smooth = savgol_filter(z, 25, 3)
plt.plot(x, z_smooth/2, 'r-')
plt.xlabel('Time')
plt.ylabel('Kinetic Energy (kCal/mol)')
plt.title('Kinetic Energy vs Time')
plt.grid()
plt.show()


me = np.median(z)
med = np.abs(z - me)
mad = np.median(med)
print("Median Absolute Deviation of Kinetic Energy: ", mad)

me = np.median(y)
med = np.abs(y - me)
mad = np.median(med)    
print("Median Absolute Deviation of Potential Energy: ", mad)

avg = np.mean(z)
std = np.std(z)
print("Standard Deviation of Kinetic Energy: ", std/avg * 100)