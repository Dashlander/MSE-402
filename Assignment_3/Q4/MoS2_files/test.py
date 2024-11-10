import re
import sys
import csv

# Ensure the filename is provided as an argument
if len(sys.argv) != 2:
    print("Usage: python script.py FILENAME")
    sys.exit(1)

# Get the filename from the command-line argument
filename = sys.argv[1]

# Open the file and read the content
try:
    with open(filename, 'r') as file:
        data = file.read()
except FileNotFoundError:
    print(f"File '{filename}' not found.")
    sys.exit(1)

# Find all instances of 'total energy' and 'estimated scf accuracy'
energy_data = re.findall(r"total energy\s+=\s+(-?\d+\.\d+)\s+Ry", data)
scf_accuracy_data = re.findall(r"estimated scf accuracy\s+<\s+(\d+\.\d+)\s+Ry", data)

# Prepare CSV file for writing
output_filename = 'extracted_data.csv'
with open(output_filename, 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    # Write header
    csvwriter.writerow(['Iteration', 'Total Energy (Ry)', 'Estimated SCF Accuracy (Ry)'])

    # Write data rows
    for i, (energy, scf_accuracy) in enumerate(zip(energy_data, scf_accuracy_data), 1):
        csvwriter.writerow([i, energy, scf_accuracy])

print(f"Data successfully written to '{output_filename}'")
