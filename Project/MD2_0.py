import numpy as np
import scipy

# Simulation parameters
n = 500                                     # number of Atoms
Edgelength_box = np.float64(5e-9)           # box length, in meters: 50 Angstroms
runtime_iterations = 5000                 # number of times the loop will run
time_step = np.float64(1e-15)               # time step = 1fs
Temp = np.float64(300)                      # Initial temperature in Kelvin

# Constants
k_b = np.float64(scipy.constants.k)         # Boltzmann constant
m_Ar = np.float64(6.642160e-26)             # mass of Argon

# Sigma and Epsilon for Argon
sigma = np.float64(3.4e-10)                 # LJ sigma for Ar
epsilon = np.float64(1.65e-21)              # LJ epsilon for Ar
cutoff_distance = np.float64(1e-9)          # cutoff distance for LJ potential

# Pre-compute LJ constants
sigma_6 = sigma ** 6
sigma_12 = sigma ** 12
epsilon_48 = 48 * epsilon
epsilon_24 = 24 * epsilon

# Initialization functions
def init_pos(n, Edgelength_box):
    return np.random.uniform(0, Edgelength_box, (n, 3))

def init_vel(n, Temp):
    vel = np.random.normal(0, np.sqrt(k_b * Temp / m_Ar), (n, 3))
    return vel - np.mean(vel, axis=0)

# Minimum image distance with broadcasting
def minimum_image_distance(r, Edgelength_box):
    delta_r = r[:, np.newaxis, :] - r[np.newaxis, :, :]
    return delta_r - Edgelength_box * np.round(delta_r / Edgelength_box)

# Lennard-Jones potential and force calculations
def lj_potential_and_force(r_ij, cutoff_distance):
    r_sq = np.sum(r_ij ** 2, axis=2)
    mask = (r_sq < cutoff_distance ** 2) & (r_sq > 0)
    
    r_6 = sigma_6 / r_sq[mask] ** 3
    r_12 = r_6 ** 2
    U = np.zeros_like(r_sq)
    F_mag = np.zeros_like(r_sq)
    
    # Lennard-Jones potential and force only for particles within cutoff
    U[mask] = 4 * epsilon * (r_12 - r_6)
    F_mag[mask] = (epsilon_48 * r_12 - epsilon_24 * r_6) / np.sqrt(r_sq[mask])
    
    return U.sum() / 2, F_mag[:, :, np.newaxis] * r_ij

# Kinetic Energy
def kinetic_energy(v):
    return 0.5 * m_Ar * np.sum(v ** 2)

# Temperature Calculation
def temperature(v):
    return 2 * kinetic_energy(v) / (3 * k_b * n)

# Function to write atom positions in .xyz format
def write_xyz(filename, r, iteration):
    with open(filename, 'a') as f:
        f.write(f"ITEM: TIMESTEP \n{iteration}\n")
        f.write(f"ITEM: NUMBER OF ATOMS\n{n}\n")
        f.write("ITEM: BOX BOUNDS pp pp pp\n")
        f.write(f"0 {Edgelength_box*1e+10}\n0 {Edgelength_box*1e+10}\n0 {Edgelength_box*1e+10}\n")
        f.write("ITEM: ATOMS id type x y z\n")
        for i in range(n):
            f.write(f"{i+1} 1 {np.round(r[i, 0]*1e+10,3)} {np.round(r[i, 1]*1e+10,3)} {np.round(r[i, 2]*1e+10,3)}\n")

# Main Loop with Velocity Verlet
def main_loop(n, Edgelength_box, runtime_iterations, time_step, Temp):
    r = init_pos(n, Edgelength_box)
    v = init_vel(n, Temp)
    
    # Initial force calculation
    r_ij = minimum_image_distance(r, Edgelength_box)
    _, F = lj_potential_and_force(r_ij, cutoff_distance)
    F_sum = F.sum(axis=1)
    
    print("Iteration", "Potential Energy", "Kinetic Energy", "Temperature")
    
    # Initialize the .xyz file
    output_filename = "dump.lammpstrj"
    with open(output_filename, 'w') as f:
        f.write(f"ITEM: TIMESTEP \n0\n")
        f.write(f"ITEM: NUMBER OF ATOMS\n{n}\n")
        f.write("ITEM: BOX BOUNDS pp pp pp\n")
        f.write(f"0 {Edgelength_box*1e+10}\n0 {Edgelength_box*1e+10}\n0 {Edgelength_box*1e+10}\n")
        f.write("ITEM: ATOMS id type x y z\n")
        for i in range(n):
            f.write(f"{i+1} 1 {np.round(r[i, 0]*1e+10,3)} {np.round(r[i, 1]*1e+10,3)} {np.round(r[i, 2]*1e+10,3)}\n")

    for iteration in range(runtime_iterations):
        # Position update
        r += v * time_step + 0.5 * (F_sum / m_Ar) * time_step ** 2
        r = r % Edgelength_box
        
        # New force calculation
        r_ij = minimum_image_distance(r, Edgelength_box)
        U, F_new = lj_potential_and_force(r_ij, cutoff_distance)
        F_sum_new = F_new.sum(axis=1)
        
        # Velocity update
        v += 0.5 * (F_sum + F_sum_new) / m_Ar * time_step
        
        # Update force for next iteration
        F_sum = F_sum_new
        
        K = kinetic_energy(v)
        T = temperature(v)
        
        if iteration % 100 == 0:
            print(iteration, U, K, T)
            write_xyz(output_filename, r, iteration)
    
    return U, K, T

U, K, T = main_loop(n, Edgelength_box, runtime_iterations, time_step, Temp)
print("Potential Energy: ", U)
print("Kinetic Energy: ", K)
print("Temperature: ", T)
