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
        "TotEng": [],
        "Press": [],
        "f_3[1]": [],
        "f_3[2]": [],
        "v_count1": [],
        "v_count2": []
    }
    
    with open(file_path, 'r') as file:
        for line in file:
            parts = line.split()
            if len(parts) == 8 and parts[0].isdigit():
                data["Step"].append(int(parts[0]))
                data["Temp"].append(float(parts[1]))
                data["TotEng"].append(float(parts[2]))
                data["Press"].append(float(parts[3]))
                data["f_3[1]"].append(float(parts[4]))
                data["f_3[2]"].append(float(parts[5]))
                data["v_count1"].append(float(parts[6]))
                data["v_count2"].append(float(parts[7]))
    
    return data

def plot_lammps_data(data):
    """
    Plots the extracted data from the LAMMPS log file.
    
    :param data: Dictionary containing the timestep and parameter data.
    """
    plt.figure(figsize=(10, 5))
    
    # Plotting Temperature
    plt.subplot(1, 2, 1)
    plt.plot(data["Step"], data["v_count1"], 'r-')
    plt.title('Number of particles of type 1')
    plt.xlabel('MC Steps')
    plt.ylabel('Number of type 1 particles')

    # Plotting Total Energy
    plt.subplot(1, 2, 2)
    plt.plot(data["Step"], data["v_count2"], 'm-')
    plt.title('Number of particles of type 2')
    plt.xlabel('MC Steps')
    plt.ylabel('Number of type 2 particles')
    plt.tight_layout()
    plt.show()
    

# Example usage
file_path = "/home/dashlander/Desktop/Sem7/CPD/Assignment_2/Q2/e10/log.lammps"  # Replace with your LAMMPS log file path
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