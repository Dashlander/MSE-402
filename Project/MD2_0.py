import numpy as np
import scipy
import time

#start time
start_time = time.time()

# Simulation parameters
n = 500                                     # number of Atoms
Edgelength_box = np.float128(2e-8)           # box length, in meters: 200 Angstroms
runtime_iterations = 100000                # number of times the loop will run
time_step = np.float128(1e-14)               # time step = 10fs
Temp = np.float128(1000)                      # Initial temperature in Kelvin
tau = np.float128(5e-14)                     # Berendsen thermostat relaxation time

# Constants
k_b = np.float128(scipy.constants.k)         # Boltzmann constant
m_Ar = np.float128(6.633853e-26)             # mass of Argon

# Sigma and Epsilon for Argon
sigma = np.float128(3.4e-10)                 # LJ sigma for Ar
epsilon = np.float128(1.65355e-21)              # LJ epsilon for Ar
cutoff_distance = np.float128(1e-9)          # cutoff distance for LJ potential

# Pre-compute LJ constants
sigma_6 = sigma ** 6
sigma_12 = sigma ** 12
epsilon_24 = 24 * epsilon
epsilon_48 = epsilon_24 * 2

#seef
np.random.seed(69)

# Initialization functions
def init_pos(n, Edgelength_box):
    mean = Edgelength_box / 2
    std_dev = Edgelength_box
    r = np.random.normal(mean, std_dev, (n, 3))
    r = r % Edgelength_box
    return r

def init_vel(n, Temp):
    vel = np.random.normal(0, np.sqrt(k_b * Temp / m_Ar), (n, 3)).astype(np.float128)
    return vel - np.mean(vel, axis=0).astype(np.float128)

# Minimum image distance with broadcasting
def minimum_image_distance(r, Edgelength_box):
    delta_r = r[:, np.newaxis, :] - r[np.newaxis, :, :]
    return delta_r - Edgelength_box * np.round(delta_r / Edgelength_box)

# Lennard-Jones potential and force calculations
def lj_potential_and_force(r_ij, cutoff_distance):
    r_sq = np.sum(r_ij ** 2, axis=2)
    np.fill_diagonal(r_sq, np.inf)
    r_inv_sq = 1 / r_sq
    r_6 = sigma_6 * r_inv_sq ** 3
    r_12 = r_6 ** 2

    pot = 4 * epsilon * (r_12 - r_6)
    F_mag = ((epsilon_48 * r_12) - (epsilon_24 * r_6)) / np.sqrt(r_sq)
    np.fill_diagonal(F_mag, 0)
    np.fill_diagonal(r_sq, np.inf)

    F = F_mag[:, :, np.newaxis] * r_ij
    return pot.sum()/2 , F

# Kinetic Energy
def kinetic_energy(v):
    return 0.5 * m_Ar * np.sum(v ** 2)

# Temperature Calculation
def temperature(v):
    return (2 * kinetic_energy(v)) / (3 * k_b * n)

#Berendsen Thermostat
def berendsen_thermostat(v, Temp, tau, time_step):
    T = temperature(v)
    lf = np.sqrt(1 + ((time_step / tau) * ((Temp / T) - 1)))
    return lf * v

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
    output_filename = "dump1.lammpstrj"
    with open(output_filename, 'w') as f:
        f.write(f"ITEM: TIMESTEP \n0\n")
        f.write(f"ITEM: NUMBER OF ATOMS\n{n}\n")
        f.write("ITEM: BOX BOUNDS pp pp pp\n")
        f.write(f"0 {Edgelength_box*1e+10}\n0 {Edgelength_box*1e+10}\n0 {Edgelength_box*1e+10}\n")
        f.write("ITEM: ATOMS id type x y z\n")
        for i in range(n):
            f.write(f"{i+1} 1 {np.round(r[i, 0]*1e+10,3)} {np.round(r[i, 1]*1e+10,3)} {np.round(r[i, 2]*1e+10,3)}\n")

    for iteration in range(runtime_iterations):
        v = v + (F_sum / m_Ar) * time_step

        r = r + v * time_step
        r = r % Edgelength_box

        r_ij = minimum_image_distance(r, Edgelength_box)
        pot, F_new = lj_potential_and_force(r_ij, cutoff_distance)
        F_sum = F_new.sum(axis=1)   # ready for next iteration's velocity update

        if iteration % 25 == 0:
            v = berendsen_thermostat(v, Temp, tau, time_step)

        if iteration % 100 == 0:
            kin = (kinetic_energy(v) * scipy.constants.N_A * 0.239) / n
            t = temperature(v)
            pot_print = (pot * scipy.constants.N_A * 0.239) / n
            print(iteration, np.round(pot_print, 5), np.round(kin, 5), np.round(t, 2))
            write_xyz(output_filename, r, iteration)
        
        if iteration % 100 == 0:
            write_xyz(output_filename, r, iteration)
    
    return pot, kin, t

pot, kin, t = main_loop(n, Edgelength_box, runtime_iterations, time_step, Temp)
print("Potential Energy: ", pot)
print("Kinetic Energy: ", kin)
print("Temperature: ", t)

end_time = time.time()
print("Time taken: ", end_time - start_time)
