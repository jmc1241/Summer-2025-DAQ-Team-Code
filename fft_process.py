"""
@name fft_process.py
@date July 18, 2025
@version 0.0.1
@notice ChatGPT was used to make this program, I did modify it.
@copyright To be decided
@brief This program allows for the CSV signal data to be processed with FFT data.
"""

# Libraries
import argparse
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys

# Get the fft values associated with the signal and the specific parameters
def FFTProcess(signal:np.array, fs:float, fmin:int, fmax:int, n:int) -> (np.ndarray, np.ndarray, np.ndarray):
    # FFT
    fft_vals = np.fft.fft(signal)
    fft_freqs = np.fft.fftfreq(n, 1/fs)

    # Positive frequencies only
    idx = np.where(fft_freqs >= 0)
    fft_freqs = fft_freqs[idx]
    fft_magnitude = np.abs(fft_vals[idx]) * 2 / n

    # Zoom range filter (if set)
    if args.fmin is not None:
        idx = fft_freqs >= args.fmin
        fft_freqs = fft_freqs[idx]
        fft_magnitude = fft_magnitude[idx]
    
    if args.fmax is not None:
        idx = fft_freqs <= args.fmax
        fft_freqs = fft_freqs[idx]
        fft_magnitude = fft_magnitude[idx]
    
    # Return all of the associated values
    return (fft_freqs, fft_magnitude, idx)

# Save all of the necessary information into a plot
def savePlot(x, y, output_file:str, title_value:str, xlabel_value:str, ylabel_value:str, color_value:str, grid_enabled:bool=True) -> None:
    # Plot
    plt.figure(figsize=(10, 6))
    plt.plot(x, y, color=color_value)
    plt.title(title_value)
    plt.xlabel(xlabel_value)
    plt.ylabel(ylabel_value)
    plt.grid(grid_enabled)
    plt.tight_layout()

    # Save figure to output file
    plt.savefig(output_file)
    print(f"FFT plot saved to {output_file}")

# Main function
if __name__ == '__main__':
    # Argparse stuff
    parser = argparse.ArgumentParser(description='Perform FFT on a CSV signal and plot the spectrum.')
    # File names
    parser.add_argument('--input_file', type=str, required=True, help='Path to input CSV file (one column of signal data).')
    parser.add_argument('--output_file', type=str, required=True, help='Path to save the output FFT plot (e.g., output.png).')
    parser.add_argument('--output_signal_file', type=str, help='Path to save the output signal plot (e.g., output_signal.png).')

    # FFT arguments
    parser.add_argument('--fs', type=float, required=True, help='Sampling frequency in Hz.')
    parser.add_argument('--fmin', type=float, help='Minimum frequency to display on the plot (Hz).')
    parser.add_argument('--fmax', type=float, help='Maximum frequency to display on the plot (Hz).')
    
    # CSV Arguments
    parser.add_argument('--column', type=int, default=0, help='Column index (0-based) of the signal in CSV.')
    parser.add_argument('--header', type=bool, default=True, help='Use this flag if the CSV has a header row.')

    
    # Arguments parsed from the console
    args = parser.parse_args()

    # Parsing the data and saving the plots for FFT
    try:
        # Load data
        if args.header:
            df = pd.read_csv(args.input_file)
        else:
            df = pd.read_csv(args.input_file, header=None)
        
        # Obtain fft parameters from the specific arguments
        signal = df.iloc[:, args.column].values
        n = len(signal)
        fs = args.fs

        fft_freqs, fft_magnitude, _ = FFTProcess(signal, fs, args.fmin, args.fmax, n)

        # Plot FFT
        savePlot(fft_freqs, fft_magnitude, args.output_file, 'FFT Spectrum', 'Frequency (Hz)', 'Amplitude', 'blue')

        # Check if we also want to save the signal to a plot
        if args.output_signal_file is not None:
            element_vector = lambda x: [i for i in range(0, x)]
            savePlot(element_vector(len(signal)), signal, args.output_signal_file, 'Signal Output', 'Time', 'Amplitude', 'red')

    # Catch CTL+C
    except KeyboardInterrupt:
        print(f"User pressed CTL+C to close out the program")

    # Catching all of the errors and letting the user know
    except Exception as e:
        print(f"Error while cleaning: {e}", file=sys.stderr)
    
    # Closeout
    finally:
        print("Exiting FFT Process")
        sys.exit(1)

