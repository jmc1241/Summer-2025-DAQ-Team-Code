# Summer 2025 Intern - DAQ CSV Toolkit
This software toolkit allows for managing & interfacing with the LabView CSV data from the NI DAQ systems to allow for signal analysis. 


## Tools
### CSV Cleaner

#### Usage
`python csv_cleaner.py --input_file signal_name.csv --output_file signal_clean.csv --time_col 0 --data_col 1 --datetime`

### FFT Process
`python fft_process.py --input_file signal_clean.csv --output_file signal_fft.png --output_signal_file signal_output.png --fs 1652 --fmax 100 --column 1`