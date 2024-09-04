import matplotlib.pyplot as plt

def parse_lammps_log(file_path):
    """
    Parses a LAMMPS log file to extract the timestep data.
    
    :param file_path: Path to the LAMMPS log file.
    :return: Dictionary containing lists of timesteps and corresponding values for each parameter.
    """
    data = {
        "Step": [],
        "Time": [],
        "CPU": [],
        "Temp": [],
        "PotEng": [],
        "KinEng": [],
        "TotEng": [],
        "Press": [],
        "Volume": []
    }
    
    with open(file_path, 'r') as file:
        for line in file:
            parts = line.split()
            if len(parts) == 9 and parts[0].isdigit():
                data["Step"].append(int(parts[0]))
                data["Time"].append(float(parts[1]))
                data["CPU"].append(float(parts[2]))
                data["Temp"].append(float(parts[3]))
                data["PotEng"].append(float(parts[4]))
                data["KinEng"].append(float(parts[5]))
                data["TotEng"].append(float(parts[6]))
                data["Press"].append(float(parts[7]))
                data["Volume"].append(float(parts[8]))
    
    return data

def plot_lammps_data(data):
    """
    Plots the extracted data from the LAMMPS log file.
    
    :param data: Dictionary containing the timestep and parameter data.
    """
    plt.figure(figsize=(10, 5))
    
    # Plotting Temperature
    plt.subplot(1, 2, 1)
    plt.plot(data["Step"], data["Temp"], 'r-')
    plt.title('Temperature vs Time')
    plt.xlabel('Step')
    plt.ylabel('Temperature')

    # Plotting Total Energy
    plt.subplot(1, 2, 2)
    plt.plot(data["Step"], data["TotEng"], 'm-')
    plt.title('Total Energy vs Time')
    plt.xlabel('Step')
    plt.ylabel('Total Energy')
    plt.tight_layout()
    plt.show()

# Example usage
file_path = "/home/dashlander/Desktop/Sem7/CPD/Assignment 1/Membrane3/log.lammps"  # Replace with your LAMMPS log file path
data = parse_lammps_log(file_path)
plot_lammps_data(data)
