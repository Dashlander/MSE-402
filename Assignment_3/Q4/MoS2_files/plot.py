import matplotlib.pyplot as plt
from matplotlib import rcParamsDefault
import numpy as np

plt.rcParams["figure.dpi"]=150
plt.rcParams["figure.facecolor"]="white"
plt.rcParams["figure.figsize"]=(8, 6)

# load data
data = np.loadtxt('MoS2.bands.dat.gnu')

k = np.unique(data[:, 0])
bands = np.reshape(data[:, 1], (-1, len(k)))

for band in range(len(bands)):
    plt.plot(k, bands[band, :], linewidth=1, alpha=0.5, color='k')
plt.xlim(min(k), max(k))

# Fermi energy
# High symmetry k-points (check bands_pp.out)
plt.axvline(0.6667, linewidth=0.75, color='k', alpha=0.5)
plt.axvline(1.0000, linewidth=0.75, color='k', alpha=0.5)
plt.axvline(1.5773, linewidth=0.75, color='k', alpha=0.5)
# text labels
plt.axhline(8.83, linewidth=0.75, color='g', alpha=0.5)
plt.axhline(8.45, linewidth=0.75, color='g', alpha=0.5)

# Text labels
plt.xticks(ticks=[0.000,0.6667, 1.0000, 1.5773], labels=['$\Gamma$', 'K', 'M', '$\Gamma$'])
plt.ylabel("Energy (eV)")
plt.title("Band Structure of MoS2")  # Add a title
plt.show()
