import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.fft import fft, fftfreq
from scipy.signal import find_peaks

# Read the CSV file
file_path = "and_f.csv"
df = pd.read_csv(file_path, delimiter=',')

# Extract time and voltage data
time = df.iloc[:, 0].values  # First column: Время[c]
voltage = df.iloc[:, 1].values  # Second column: Напряжение[В]

# Remove NaN values if any
mask = ~np.isnan(voltage)
time = time[mask]
voltage = voltage[mask]

# Compute Fourier Transform
N = len(time)
T = time[1] - time[0]  # Sampling period

# Perform FFT
yf = fft(voltage)
xf = fftfreq(N, T)[:N//2]  # Positive frequencies only

# Calculate magnitude spectrum
magnitude = 2.0/N * np.abs(yf[:N//2])

# Find dominant frequencies
peaks, properties = find_peaks(magnitude, height=0.01*np.max(magnitude))
dominant_freqs = xf[peaks]
dominant_mags = magnitude[peaks]

# Sort by magnitude in descending order
sorted_indices = np.argsort(dominant_mags)[::-1]
dominant_freqs = dominant_freqs[sorted_indices]
dominant_mags = dominant_mags[sorted_indices]

# Reconstruct signal using dominant frequencies
def reconstruct_signal(t, dominant_freqs, dominant_mags, yf, N):
    """
    Reconstruct signal using inverse Fourier transform with selected frequencies
    """
    reconstructed = np.zeros_like(t, dtype=complex)
    
    for freq, mag in zip(dominant_freqs[:10], dominant_mags[:10]):  # Use top 10 frequencies
        k = np.where(np.abs(xf - freq) < 1e-6)[0][0]
        reconstructed += mag * np.exp(2j * np.pi * freq * t)
    
    return reconstructed.real

# Reconstruct the signal
reconstructed = reconstruct_signal(time, dominant_freqs, dominant_mags, yf, N)

# Print results
print("="*60)
print("FOURIER DECOMPOSITION RESULTS")
print("="*60)
print(f"Total samples: {N}")
print(f"Sampling period: {T:.6f} s")
print(f"Sampling frequency: {1/T:.2f} Hz")
print(f"Time range: {time[0]:.4f} to {time[-1]:.4f} s")
print(f"Signal duration: {time[-1] - time[0]:.4f} s")
print("\n" + "="*60)
print("TOP 10 DOMINANT FREQUENCY COMPONENTS")
print("="*60)
print(f"{'Rank':<6} {'Frequency (Hz)':<20} {'Magnitude':<15} {'Period (s)':<15}")
print("-"*60)

for i, (freq, mag) in enumerate(zip(dominant_freqs[:10], dominant_mags[:10]), 1):
    if freq > 0:  # Skip DC component (0 Hz)
        period = 1/freq if freq != 0 else float('inf')
        print(f"{i:<6} {freq:<20.4f} {mag:<15.6f} {period:<15.6f}")

print("\n" + "="*60)
print("STATISTICAL ANALYSIS")
print("="*60)
print(f"Original signal mean: {np.mean(voltage):.6f} V")
print(f"Reconstructed signal mean: {np.mean(reconstructed):.6f} V")
print(f"Original signal std: {np.std(voltage):.6f} V")
print(f"Reconstructed signal std: {np.std(reconstructed):.6f} V")
print(f"Reconstruction error (MSE): {np.mean((voltage - reconstructed)**2):.6e}")

# Plotting
fig, axes = plt.subplots(2, 2, figsize=(15, 10))

# 1. Original signal
axes[0, 0].plot(time, voltage, 'b-', alpha=0.7, linewidth=1)
axes[0, 0].set_xlabel('Time [s]')
axes[0, 0].set_ylabel('Voltage [V]')
axes[0, 0].set_title('Original Signal')
axes[0, 0].grid(True, alpha=0.3)

# 2. Frequency spectrum
axes[0, 1].plot(xf, magnitude, 'g-', linewidth=1)
axes[0, 1].plot(dominant_freqs[:10], dominant_mags[:10], 'ro', markersize=8, 
                label='Top 10 frequencies')
axes[0, 1].set_xlabel('Frequency [Hz]')
axes[0, 1].set_ylabel('Magnitude')
axes[0, 1].set_title('Frequency Spectrum')
axes[0, 1].set_xlim([0, min(100, np.max(xf))])  # Limit to 100 Hz for clarity
axes[0, 1].grid(True, alpha=0.3)
axes[0, 1].legend()

# 3. Reconstructed signal
axes[1, 0].plot(time, reconstructed, 'r-', alpha=0.7, linewidth=1)
axes[1, 0].set_xlabel('Time [s]')
axes[1, 0].set_ylabel('Voltage [V]')
axes[1, 0].set_title(f'Reconstructed Signal (Top {min(10, len(dominant_freqs))} frequencies)')
axes[1, 0].grid(True, alpha=0.3)

# 4. Comparison
axes[1, 1].plot(time, voltage, 'b-', alpha=0.5, linewidth=1, label='Original')
axes[1, 1].plot(time, reconstructed, 'r-', alpha=0.7, linewidth=1, label='Reconstructed')
axes[1, 1].set_xlabel('Time [s]')
axes[1, 1].set_ylabel('Voltage [V]')
axes[1, 1].set_title('Original vs Reconstructed Signal')
axes[1, 1].legend()
axes[1, 1].grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

# Additional detailed analysis
print("\n" + "="*60)
print("DETAILED FREQUENCY ANALYSIS")
print("="*60)

# Find DC component (0 Hz)
dc_index = np.argmin(np.abs(xf))
dc_component = magnitude[dc_index]
print(f"DC component (0 Hz): {dc_component:.6f} V")

# Find main frequency (largest non-DC component)
if len(dominant_freqs) > 1:
    main_freq = dominant_freqs[1]  # Skip DC
    main_mag = dominant_mags[1]
    print(f"Main frequency: {main_freq:.4f} Hz")
    print(f"Main frequency magnitude: {main_mag:.6f} V")
    print(f"Main period: {1/main_freq:.6f} s")

# Calculate total power
total_power = np.sum(magnitude**2)
print(f"Total signal power: {total_power:.6e} V²")

# Calculate power in top 10 frequencies
top10_power = np.sum(dominant_mags[:10]**2)
power_ratio = top10_power / total_power * 100
print(f"Power in top 10 frequencies: {top10_power:.6e} V² ({power_ratio:.2f}% of total)")

# Save results to file
results_df = pd.DataFrame({
    'Frequency_Hz': dominant_freqs[:20],
    'Magnitude_V': dominant_mags[:20],
    'Period_s': [1/f if f > 0 else float('inf') for f in dominant_freqs[:20]]
})

results_df.to_csv('fourier_analysis_results.csv', index=False)
print(f"\nDetailed results saved to 'fourier_analysis_results.csv'")

# Optional: Plot phase information
phase = np.angle(yf[:N//2])
fig2, ax2 = plt.subplots(1, 2, figsize=(12, 5))

# Phase spectrum
ax2[0].plot(xf, phase, 'b-', alpha=0.7, linewidth=1)
ax2[0].set_xlabel('Frequency [Hz]')
ax2[0].set_ylabel('Phase [rad]')
ax2[0].set_title('Phase Spectrum')
ax2[0].grid(True, alpha=0.3)

# Log-scale magnitude spectrum
ax2[1].semilogy(xf, magnitude, 'g-', linewidth=1)
ax2[1].set_xlabel('Frequency [Hz]')
ax2[1].set_ylabel('Magnitude [V] (log scale)')
ax2[1].set_title('Frequency Spectrum (Log Scale)')
ax2[1].grid(True, alpha=0.3)

plt.tight_layout()
plt.show()
