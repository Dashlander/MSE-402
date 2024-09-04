import matplotlib.pyplot as plt

def count_atoms_below_z(file_path, atom_type, z_threshold):
    """
    Reads a LAMMPS dump file and counts the number of atoms of a specific type with z < z_threshold at each timestep.
    
    :param file_path: Path to the LAMMPS dump file.
    :param atom_type: The atom type to track.
    :param z_threshold: The z-coordinate threshold.
    :return: Dictionary with timesteps as keys and counts as values.
    """
    counts = {}
    with open(file_path, 'r') as file:
        timestep = None
        reading_atoms = False
        
        for line in file:
            if line.startswith("ITEM: TIMESTEP"):
                timestep = int(next(file).strip())
                counts[timestep] = 0  # Initialize count for the current timestep
                reading_atoms = False  # Reset the flag for reading atoms
            elif line.startswith("ITEM: ATOMS"):
                reading_atoms = True  # Set the flag to start reading atoms
            elif reading_atoms:
                data = line.split()
                current_atom_type = int(data[1])
                z = float(data[4])
                if current_atom_type == atom_type and z < z_threshold:
                    counts[timestep] += 1
    
    return counts

def plot_atom_counts(counts):
    """
    Plots the number of atoms against timesteps.
    
    :param counts: Dictionary with timesteps as keys and counts as values.
    """
    timesteps = list(counts.keys())
    atom_counts = list(counts.values())

    plt.figure(figsize=(10, 6))
    plt.plot(timesteps, atom_counts, linestyle='-', color='b')
    plt.title("Number of Carbon DiOxide Diffused through Membrane 1")
    plt.xlabel("Time")
    plt.ylabel("Number of Molecules")
    plt.xlim(-100,505000)
    plt.ylim(-0.1,1.5)
    plt.grid(False)
    plt.show()

# Example usage
file_path = "/home/dashlander/Desktop/Sem7/CPD/Assignment 1/Q5/Mem1/dump.lammpstrj"  # Replace with your dump file path
atom_type = 2  # The atom type you're interested in
z_threshold = 0  # z-coordinate threshold
counts = count_atoms_below_z(file_path, atom_type, z_threshold)

# Plot the results
plot_atom_counts(counts)
