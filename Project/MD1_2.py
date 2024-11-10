import numpy as np
import scipy.constants as const

# Simulation parametrs
n = 500                                 # Number of atoms
Edgelength_box = np.float64(5e-8)       # Box length, in metres: 500 Angstroms
runtime_iterations = 1000               # Number of time steps
time_step = np.float64(1e-15)           # Time step = 1fs
Temp = np.float64(300)                  # Initial temperature in Kelvin

# Constants
k_b = np.float64(const.k)               # Boltzmann constant
m_Ar = np.float64(6.642160e-26)         # Mass of Ar

# LJ Parameters for Argon
sigma = np.float64(3.4e-10)
epsilon = np.float64(1.65e-21)
cutoff_distance = np.float64(1e-9)

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
    return vel - np.mean(vel, axis=0) #This is for ensuring the mean velocity is zero, so that the momentum of the system is zero

# Minimum image distance with broadcasting : (n, 3) - (n, 1, 3) = (n, n, 3)
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

# Main Loop
def main_loop(n, Edgelength_box, runtime_iterations, time_step, Temp):
    r = init_pos(n, Edgelength_box)
    v = init_vel(n, Temp)
    print("Iteration", "Potential Energy", "Kinetic Energy", "Temperature")
    
    for _ in range(runtime_iterations):
        r_ij = minimum_image_distance(r, Edgelength_box)
        U, F = lj_potential_and_force(r_ij, cutoff_distance)
        F_sum = F.sum(axis=1)

        v += (F_sum / m_Ar) * time_step
        r += v * time_step
        K = kinetic_energy(v)
        T = temperature(v)

        if _ % 100 == 0:
            print(_, U, K, T)
    
    return U, K, T

U, K, T = main_loop(n, Edgelength_box, runtime_iterations, time_step, Temp)
print("Potential Energy: ", U)
print("Kinetic Energy: ", K)
print("Temperature: ", T)
