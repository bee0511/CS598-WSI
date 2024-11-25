import numpy as np
import matplotlib.pyplot as plt
from scipy.io import loadmat
import os

def create_output_directory(output_dir):
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    return output_dir

def load_data():
    try:
        data = loadmat('h_static.mat')
        h = data['h']  # 100x2 matrix for two antennas
        t = data['t'].flatten()  # timestamps
        return h, t
    except Exception as e:
        print(f"Error loading data: {e}")
        return None, None

def plot_antenna1_phase(h, t, output_dir):
    phase_ant1 = np.angle(h[:, 0], deg=True)  # Convert to degrees
    
    plt.figure(figsize=(10, 6))
    plt.plot(t, phase_ant1, 'b.-')
    plt.xlabel('Time (ms)')
    plt.ylabel('Phase (degrees)')
    plt.title('Channel Phase vs Time for Antenna 1')
    plt.grid(True)
    
    # Save figure
    plt.savefig(os.path.join(output_dir, 'antenna1_phase.png'), 
                dpi=300, bbox_inches='tight')
    plt.close()  # Close the figure to free memory
    
    return phase_ant1

def plot_antenna_ratio_phase(h, t, output_dir):
    # Calculate phase of ratio between antenna 1 and antenna 2
    phase_ratio = np.angle(h[:, 0] / h[:, 1], deg=True)
    
    plt.figure(figsize=(10, 6))
    plt.plot(t, phase_ratio, 'r.-')
    plt.xlabel('Time (ms)')
    plt.ylabel('Phase Ratio (degrees)')
    plt.title('Phase Ratio between Antennas vs Time')
    plt.grid(True)
    
    # Save figure
    plt.savefig(os.path.join(output_dir, 'phase_ratio.png'), 
                dpi=300, bbox_inches='tight')
    plt.close()  # Close the figure to free memory
    
    return phase_ratio

def main():
    output_dir = 'figures'
    
    create_output_directory(output_dir)
    print(f"Output directory created/verified: {output_dir}")
    
    print("Loading channel measurement data...")
    h, t = load_data()
    
    if h is None or t is None:
        return
    
    print("\nGenerating plots and analysis...")
    
    # Plot phase of antenna 1
    print("\nPlotting and saving antenna 1 phase...")
    plot_antenna1_phase(h, t, output_dir)
    
    # Plot phase ratio
    print("\nPlotting and saving phase ratio...")
    plot_antenna_ratio_phase(h, t, output_dir)
    
    print(f"\nAnalysis complete! All files have been saved to the '{output_dir}' directory.")
    print("Files generated:")
    print("1. antenna1_phase.png - Phase plot for antenna 1")
    print("2. phase_ratio.png - Phase ratio plot")

if __name__ == "__main__":
    main()