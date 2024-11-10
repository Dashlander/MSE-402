import numpy as np
import scipy
import matplotlib.pyplot as plt

#simulation paramters
n = 500                                     #number of Atoms
Edgelength_box = np.float64(5e-8)           #box length, in metres: 500 Angstroms
runtime_iterations = 1000                   #number of times the loop will run
time_step = np.float64(1e-15)               #time step = 1fs
Temp = np.float64(300)                      #Initial temperature in Kelvin

#constants
k_b = np.float64(scipy.constants.k)         #Boltzmann constant
m_Ar = np.float64(6.642160e-26)             #mass of Arg

#sigma and Epsilon for Argon
sigma = np.float64(3.4e-10)                #LJ sigma for Ar
epsilon = np.float64(1.65e-21)             #LJ epsilon for Ar
cutoff_distance = np.float64(1e-9)         #cutoff distance for LJ potential, normally taken as 2.5*sigma, which would be 8.5 in this case, but I am using 10 for simplicity

#initialisation functions
def init_pos(n, Edgelength_box): #vectors of random positions
    return np.random.uniform(0, Edgelength_box, (n, 3))

def init_vel(n, Temp): # Use Maxwell Boltzmann distribution
    vel = np.random.normal(0, np.sqrt(k_b * Temp / m_Ar), (n, 3))
    vel = vel - np.mean(vel, axis=0) #This is for ensuring the mean velocity is zero, so that the momentum of the system is zero
    return vel

#Min Image Distance
def minimum_image_distance(r_i, r_j, Edgelength_box):
    r_ij = r_i - r_j
    r_ij = r_ij - Edgelength_box * np.round(r_ij / Edgelength_box)
    return r_ij

#Force Calculation
def lj_force(r_ij, epsilon, sigma, cutoff_distance):
    r = np.linalg.norm(r_ij)
    if r < cutoff_distance:
        return 48 * epsilon * np.power(sigma, 12) / np.power(r, 13) - 24 * epsilon * np.power(sigma, 6) / np.power(r, 7)
    else:
        return np.float64(0.0)

#Potential Energy Calculation
def lj_potential(r_ij, epsilon, sigma, cutoff_distance):
    r = np.linalg.norm(r_ij)
    if r < cutoff_distance:
        return 4 * epsilon * (np.power(sigma / r, 12) - np.power(sigma / r, 6))
    else:
        return np.float64(0.0)

#Kinetic Energy Calculation
def kinetic_energy(v):
    return 0.5 * m_Ar * np.sum(np.linalg.norm(v, axis=1) ** 2)

#Temperature Calculation
def temperature(v):
    return 2 * kinetic_energy(v) / (3 * k_b * n)

#Main Loop
def main_loop(n, Edgelength_box, runtime_iterations, time_step, Temp):
    r = init_pos(n, Edgelength_box)
    v = init_vel(n, Temp)
    F = np.zeros((n, 3))
    U = 0
    K = 0
    T = 0
    print("iteration", "Potential Energy", "Kinetic Energy", "Temperature")
    for _ in range(runtime_iterations):
        U = 0
        for i in range(n):
            for j in range(i + 1, n):
                r_ij = minimum_image_distance(r[i], r[j], Edgelength_box)
                F_ij = lj_force(r_ij, epsilon, sigma, cutoff_distance)
                if F_ij != 0:
                    F[i] += F_ij * r_ij / np.linalg.norm(r_ij)
                    F[j] -= F_ij * r_ij / np.linalg.norm(r_ij)
                    U += lj_potential(r_ij, epsilon, sigma, cutoff_distance)
        v += F / m_Ar * time_step
        r += v * time_step
        F = np.zeros((n, 3))            # reset forces
        K = kinetic_energy(v)           # calculate kinetic energy
        T = temperature(v)              # calculate temperature
        print (_, U, K, T)              # print results
    return U, K, T

U, K, T = main_loop(n, Edgelength_box, runtime_iterations, time_step, Temp)
print("Potential Energy: ", U)
print("Kinetic Energy: ", K)
print("Temperature: ", T)