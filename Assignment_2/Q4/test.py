import numpy as np
import matplotlib.pyplot as plt

# Function to read binary data from a file and convert it to a numpy array
def read_binary_file(filepath):
    with open(filepath, 'r') as f:
        lines = f.readlines()
        data = [[int(x) for x in line.split()] for line in lines]
        return np.array(data)


# List of file paths
file_paths = [
    "fort.11",
    "fort.12",
    "fort.13",
    "fort.14",
    "fort.15",
    "fort.16",
    "fort.17",
    "fort.18",
    "fort.19",
    "fort.20",
    "fort.21",
    "fort.22",
    "fort.23",
    "fort.24",
    "fort.25",
    "fort.26",
    "fort.27",
    "fort.28",
    "fort.29",
]

# Loop through each file, plot, and save it as a PNG image
for filepath in file_paths:
    # Read binary data from file
    data = read_binary_file(filepath)
    
    # Plot the data
    plt.imshow(data, cmap='gray')  # Adjust cmap if necessary
    plt.title(filepath)  # Set title as filename  # Add color bar if needed
    plt.savefig(filepath + '.png')  # Save the plot as a PNG image
    plt.close()  # Close the plot to avoid memory issues
