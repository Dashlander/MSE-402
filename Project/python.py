import numpy as np
import matplotlib.pyplot as plt
from multiprocessing import Pool

def read_dump(file):
    """Reads a LAMMPS dump file and extracts atom positions for all timesteps."""
    frames = []
    box_bounds = None

    with open(file, "r") as f:
        lines = f.readlines()

    frame = []
    for i, line in enumerate(lines):
        if "ITEM: TIMESTEP" in line:
            if frame:  # Save the current frame if it exists
                frames.append(np.array(frame))
                frame = []
        elif "ITEM: BOX BOUNDS" in line:
            # Read box bounds (assumes cubic box with periodic boundaries)
            box_bounds = [float(bound.split()[1]) for bound in lines[i + 1:i + 4]]
        elif "ITEM: ATOMS" in line:
            # Start reading atom positions
            j = i + 1
            while j < len(lines) and "ITEM:" not in lines[j]:
                frame.append(list(map(float, lines[j].split()[2:5])))  # Extract x, y, z
                j += 1

    if frame:  # Add the last frame
        frames.append(np.array(frame))

    return frames, box_bounds[1]  # Return frames and box length

def compute_distances(frame, box_length):
    """Computes pairwise distances between atoms, applying periodic boundary conditions."""
    n_atoms = len(frame)
    
    # Use numpy broadcasting to compute pairwise distances
    frame = np.array(frame)
    diff = frame[:, np.newaxis, :] - frame[np.newaxis, :, :]  # shape (n_atoms, n_atoms, 3)
    
    # Apply periodic boundary conditions
    diff -= box_length * np.round(diff / box_length)
    
    # Compute the distance matrix
    dist_matrix = np.linalg.norm(diff, axis=2)
    
    # Extract upper triangle (avoiding double counting)
    i, j = np.triu_indices(n_atoms, k=1)
    return dist_matrix[i, j]

def calculate_rdf(frames, box_length, bins=200, r_max=10.0):
    """Calculate the RDF using multiprocessing and efficient pairwise distance calculation."""
    bin_edges = np.linspace(0, r_max, bins + 1)
    dr = bin_edges[1] - bin_edges[0]
    g_r = np.zeros(bins)
    volume = box_length ** 3
    rho = len(frames[0]) / volume  # Number density
    
    # Create a pool of workers to parallelize over timesteps
    with Pool() as pool:
        # Compute pairwise distances in parallel for all frames
        distances_list = pool.starmap(compute_distances, [(frame, box_length) for frame in frames])
    
    # Flatten the distances list and calculate the RDF
    all_distances = np.concatenate(distances_list)
    
    # Histogram the distances
    hist, _ = np.histogram(all_distances, bins=bin_edges)
    
    # Correctly normalize the RDF: Divide by the number density, volume, and bin factors
    bin_volume = 4 * np.pi * bin_edges[:-1]**2 * dr  # Volume of the spherical shell for each bin
    norm_factor = rho * bin_volume  # Normalization factor
    
    g_r = hist / norm_factor  # Normalize the histogram counts
    return bin_edges[:-1] + dr / 2, g_r

def calculate_rdf_for_frame(frame, box_length, bins=200, r_max=10.0):
    """Calculate the RDF for a single frame."""
    bin_edges = np.linspace(0, r_max, bins + 1)
    dr = bin_edges[1] - bin_edges[0]
    g_r = np.zeros(bins)
    volume = box_length ** 3
    rho = len(frame) / volume  # Number density
    
    # Compute pairwise distances for the current frame
    distances = compute_distances(frame, box_length)
    
    # Histogram the distances
    hist, _ = np.histogram(distances, bins=bin_edges)
    
    # Normalize the RDF for the frame
    bin_volume = 4 * np.pi * bin_edges[:-1]**2 * dr  # Volume of the spherical shell for each bin
    norm_factor = rho * bin_volume  # Normalization factor
    
    g_r = hist / norm_factor  # Normalize the histogram counts
    return bin_edges[:-1] + dr / 2, g_r

# Load dump file and calculate RDF with corrected normalization
dump_file = "dump2.lammpstrj"
frames, box_length = read_dump(dump_file)

# Calculate time-averaged RDF for all frames
r, g_r = calculate_rdf(frames, box_length, bins=200)

# Choose specific time steps (e.g., 0, 10, 20, etc.)
specific_time_steps = [0,9,19,49]  # Example time steps you want RDF for
r_specific = []
g_r_specific = []

# Calculate RDF for the specific frames
for timestep in specific_time_steps:
    frame = frames[timestep]
    r_frame, g_r_frame = calculate_rdf_for_frame(frame, box_length, bins=200)
    r_specific.append(r_frame)
    g_r_specific.append(g_r_frame)

# Plot RDFs
plt.figure()
plt.plot(r/3.405, (g_r/250000), label="Time-Averaged RDF", color='blue', linewidth = 1.5)

#Plot RDF for specific frames
#for i, timestep in enumerate(specific_time_steps):
#    plt.plot(r_specific[i]/3.405, g_r_specific[i]/2000, label=f"RDF at Timestep {(timestep + 1) * 100}", linewidth = 0.5)

plt.xlabel("r / \u03C3")
plt.ylabel("g(r)")
plt.title("Radial Distribution Function")
plt.grid()
plt.show()