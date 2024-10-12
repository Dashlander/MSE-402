import matplotlib.pyplot as plt

def read_file(filename):
    mc_steps = []
    energies = []

    with open(filename, 'r') as file:
        for line in file:
            if line.startswith("#") or line.strip() == "":  # Skip comment and empty lines
                continue
            
            parts = line.split()
            if len(parts) >= 2:
                mc_step = int(parts[0])  # First column is MC_STEP
                energy_total = float(parts[1])  # Second column is Energy_Total

                mc_steps.append(mc_step)
                energies.append(energy_total)

    return mc_steps, energies

def plot_data(mc_steps, energies):
    plt.figure(figsize=(10, 6))
    plt.plot(mc_steps, energies, 'r-')
    plt.title('MC_Steps vs Energy')
    plt.xlabel('MC_Steps')
    plt.ylabel('Energy (kJ/mol)')
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    # Replace 'data.txt' with the path to your file
    mc_steps, energies = read_file('Graphene_H2O.prp')
    plot_data(mc_steps, energies)
