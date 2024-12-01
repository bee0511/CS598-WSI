import numpy as np
import scipy.io
import matplotlib.pyplot as plt

# Load data from the .mat file
data = scipy.io.loadmat('circular.mat')
h = data['h']  # Channel measurements (complex values)
t = data['t'].flatten()  # Timestamps (milliseconds)

# Constants
R = 20.8e-2  # Radius in meters
frequency = 5.5e9  # Frequency in Hz
wavelength = 3e8 / frequency  # Calculate wavelength
angular_velocity = 2 * np.pi / 12.25  # Radians per second

# Calculate angular positions (phi_k) using timestamps
phi = angular_velocity * (t - t[0]) / 1000  # Convert to seconds

# Define the theta' range
theta_range = np.linspace(-180, 180, 361)  # In degrees
theta_radians = np.radians(theta_range)  # Convert to radians

# Initialize the multipath profile array
P = []

# Compute multipath profile using the given formula
for i, theta_prime in enumerate(theta_radians):
    phase_compensation = np.exp(-1j * 2 * np.pi *
                                R * np.cos(phi - theta_prime) / wavelength)
    P.append(np.abs(np.sum(h[:, 1] / h[:, 0] * phase_compensation)
                    )**2)  # Ratio compensates offsets

# Load validation data from MultipathProfile.mat
validation_data = scipy.io.loadmat('MultipathProfile.mat')
P_validation = validation_data['P'].flatten()  # Validation power values
# Corresponding angles
theta_validation = np.linspace(-180, 180, len(P_validation))

# Plot the computed multipath profile and validation data
plt.figure(figsize=(10, 6))
plt.plot(theta_range, P, label='Computed Profile', color='blue')
plt.plot(theta_validation, P_validation,
         label='Validation Profile', linestyle='--', color='red')
plt.title('Multipath Profile Comparison')
plt.xlabel('Angle θ′ (degrees)')
plt.ylabel('Power P(θ′)')
plt.legend()
plt.grid()

# Save the plot to the figures directory
plt.savefig('figures/multipath_profile_comparison.png')

plt.show()
