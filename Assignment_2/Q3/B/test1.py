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
                x = float(data[2])
                y = float(data[3])
                z = float(data[4])
                if current_atom_type == atom_type and (-5.512084438507452 < x < 26.09766215010596) and (-0.12771230207837192 < y < 20.71329001367807) and (3.211752393088563 < z < 17.373825318513106):
                    counts[timestep] += 1
    
    return counts

# Example usage
file_path = "/home/dashlander/Desktop/Sem7/CPD/Assignment_2/Q3/B/dump.lammpstrj"  # Replace with your dump file path
atom_type = 3  # The atom type you're interested in
z_threshold = 0  # z-coordinate threshold
counts = count_atoms_below_z(file_path, atom_type, z_threshold)

# Display counts for each timestep
for timestep, count in counts.items():
    print(f"Timestep: {timestep}, Count of atoms of type {atom_type} inside the crack: {count}")
