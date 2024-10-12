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
        "Press": [],
        "PotEng" : [],
        "KinEng" : [],
        "Density" : [],
        "Atoms" : [],
        "v_iacc" : [],
        "v_dacc" : [],
        "v_tacc" : [],
        "v_racc" : [],
        "v_nO" : [],
        "v_nH" : []
    }
    
    with open(file_path, 'r') as file:
        for line in file:
            parts = line.split()
            if len(parts) == 13 and parts[0].isdigit():
                data["Step"].append(int(parts[0]))
                data["Temp"].append(float(parts[1]))
                data["Press"].append(float(parts[2]))
                data["PotEng"].append(float(parts[3]))
                data["KinEng"].append(float(parts[4]))
                data["Density"].append(float(parts[5]))
                data["Atoms"].append(int(parts[6]))
                data["v_iacc"].append(float(parts[7]))
                data["v_dacc"].append(float(parts[8]))
                data["v_tacc"].append(int(parts[9]))
                data["v_racc"].append(int(parts[10]))
                data["v_nO"].append(int(parts[11]))
                data["v_nH"].append(int(parts[12]))
    
    return data

def plot_lammps_data(data):
    """
    Plots the extracted data from the LAMMPS log file.
    
    :param data: Dictionary containing the timestep and parameter data.
    """
    plt.plot(data["Step"], data["Density"], 'r-')
    plt.xlabel('MC Steps')
    plt.ylabel('Density')
    plt.tight_layout()
    plt.show()

    plt.plot(data["Step"], data["v_nO"], 'g-')
    plt.xlabel('MC Steps')
    plt.ylabel('Number of Oxygen Atoms')
    plt.tight_layout()
    plt.show()

    plt.plot(data["Step"], data["v_nH"], 'b-')
    plt.xlabel('MC Steps')
    plt.ylabel('Number of Hydrogen Atoms')
    plt.tight_layout()
    plt.show()
    

# Example usage
file_path = "/home/dashlander/Desktop/Sem7/CPD/Assignment_2/Q3/A/log.lammps"  # Replace with your LAMMPS log file path
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