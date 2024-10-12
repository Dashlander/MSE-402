import matplotlib.pyplot as plt

def parse_lammps_log(file_path):
    """
    Parses a LAMMPS log file to extract the timestep data.
    
    :param file_path: Path to the LAMMPS log file.
    :return: Dictionary containing lists of timesteps and corresponding values for each parameter.
    """
    data = {
        "Step": [],
        "Temp": [],
        "E_pair" : [],
        "E_mol" : [],
        "TotEng" : [],
        "Press": []
    }
    
    with open(file_path, 'r') as file:
        for line in file:
            parts = line.split()
            if len(parts) == 6 and parts[0].isdigit():
                data["Step"].append(int(parts[0]))
                data["Temp"].append(float(parts[1]))
                data["E_pair"].append(float(parts[2]))
                data["E_mol"].append(float(parts[3]))
                data["TotEng"].append(float(parts[4]))
                data["Press"].append(float(parts[5]))

    return data

def plot_lammps_data(data):
    """
    Plots the extracted data from the LAMMPS log file.
    
    :param data: Dictionary containing the timestep and parameter data.
    """
    plt.plot(data["Step"], data["TotEng"], 'r-')
    plt.xlabel('MC Steps')
    plt.ylabel('Energy')
    plt.tight_layout()
    plt.show()

    

# Example usage
file_path = "/home/dashlander/Desktop/Sem7/CPD/Assignment_2/Q3/B/log.lammps"  # Replace with your LAMMPS log file path
data = parse_lammps_log(file_path)
plot_lammps_data(data)

"""
# Plotting Temperature
plt.plot(data["Step"], data["v_count1"], 'r-')
plt.plot(data["Step"], data["v_count2"], 'm-')
plt.xlabel('MC Steps')
plt.ylabel('Number of particles')
plt.tight_layout()
plt.show() """