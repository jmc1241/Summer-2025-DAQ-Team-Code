"""
@name csv_cleaner.py
@date July 18, 2025
@version 0.0.1
@notice ChatGPT was used to make this program, I did modify it.
@copyright To be decided
@brief This program allows for LabView data of CSV files to be cleaned up since sometimes LabView
sometimes has a hard time putting data into a file properly. 
"""
# Libraries
import argparse
import pandas as pd
import sys

# Main program management
if __name__ == '__main__':
    # Argparse 
    parser = argparse.ArgumentParser(description='Clean and sanitize LabView-style CSV data.')
    parser.add_argument('--input_file', type=str, required=True, help='Path to the input CSV file (LabView style).')
    parser.add_argument('--output_file', type=str, required=True, help='Path to save the cleaned CSV file.')
    parser.add_argument('--time_col', type=int, default=0, help='Index of the time column (default: 0).')
    parser.add_argument('--data_col', type=int, default=1, help='Index of the data column (default: 1).')
    parser.add_argument('--datetime', action='store_true', help='Convert time strings to datetime objects.')

    # Arguments associated with argparse
    args = parser.parse_args()

    # Starting the csv cleanup process (with error handling)
    try:
        # Read the CSV file
        df = pd.read_csv(args.input_file, header=None)

        # Extract and rename columns for clarity
        time_col = df.iloc[:, args.time_col]
        data_col = df.iloc[:, args.data_col]

        # Attempt to convert data to float (invalid entries become NaN)
        data_col_clean = pd.to_numeric(data_col, errors='coerce')

        # Optional: parse time string to datetime
        if args.datetime:
            time_col = pd.to_datetime(time_col, errors='coerce')  # invalid dates → NaT

        # Combine into cleaned DataFrame
        cleaned_df = pd.DataFrame({
            'time': time_col,
            'value': data_col_clean
        })

        # Drop rows with invalid data or time
        cleaned_df = cleaned_df.dropna()

        # Save cleaned data
        cleaned_df.to_csv(args.output_file, index=False)
        print(f"Cleaned data saved to {args.output_file}")
    
    # Catch CTL+C
    except KeyboardInterrupt:
        print(f"User pressed CTL+C to close out the program")

    # Catching all of the errors and letting the user know
    except Exception as e:
        print(f"Error while cleaning: {e}", file=sys.stderr)
    
    # Closeout
    finally:
        print("Exiting CSV Cleaner")
        sys.exit(1)
