import numpy as np
import matplotlib.pyplot as plt
from scipy.io import loadmat

def load_channel_data(filename):
    data = loadmat(filename)
    h1 = data['h1']
    h2 = data['h2']
    t1 = data['t1'].flatten()
    t2 = data['t2'].flatten()
    
    # Ensure h1 and h2 have the same shape
    min_length = min(h1.shape[0], h2.shape[0])
    h1 = h1[:min_length]
    h2 = h2[:min_length]
    t1 = t1[:min_length]
    t2 = t2[:min_length]
    
    return h1, h2, t1, t2

def analyze_phase_difference(h1, h2, t1, t2):
    # Calculate the phase difference between the antennas
    phase_diff_h1 = np.unwrap(np.angle(h1[:, 0] / h1[:, 1]))
    phase_diff_h2 = np.unwrap(np.angle(h2[:, 0] / h2[:, 1]))
    # Plot the phase difference for h1
    plt.figure()
    plt.plot(t1, phase_diff_h1, label='Phase Difference (h1)')
    plt.xlabel('Time')
    plt.ylabel('Phase Difference (radians)')
    plt.title('Phase Difference between Antennas (h1)')
    plt.legend()
    plt.grid(True)
    plt.savefig('figures/phase_difference_h1.png')
    plt.close()
    
    # Plot the phase difference for h2
    plt.figure()
    plt.plot(t2, phase_diff_h2, label='Phase Difference (h2)')
    plt.xlabel('Time')
    plt.ylabel('Phase Difference (radians)')
    plt.title('Phase Difference between Antennas (h2)')
    plt.legend()
    plt.grid(True)
    plt.savefig('figures/phase_difference_h2.png')
    plt.close()

def main():
    """
    Main function to execute the analysis
    """
    print("Loading channel measurement data...")
    h1, h2, t1, t2 = load_channel_data('h_move.mat')
    
    print("\nAnalyzing phase difference to determine Roomba motion direction...")
    analyze_phase_difference(h1, h2, t1, t2)
if __name__ == "__main__":
    main()