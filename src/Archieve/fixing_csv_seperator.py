import pandas as pd
import os

# --- Configuration ---
# Your file path
input_file_path = r'C:\Users\stefa\Pycharm_CIP_Jobs_Project_Github\data\processed\jobs_ch_skills_all_cleaned_final_V1.csv'

# Define the path for the corrected output file
# It's always best practice to save the corrected version as a new file.
output_file_path = input_file_path.replace('.csv', '_semicolon_fixed.csv')

# Read the problematic file correctly
try:
    print(f"Reading file: {input_file_path}")

    df = pd.read_csv(
        input_file_path,
        sep=',',
        quotechar='"',
        encoding='utf-8'  # Ensures proper handling of characters (e.g., German umlauts)
    )

    print("✅ Data successfully loaded with correct column separation.")
    print("-" * 50)
    print("First 5 rows (confirming structure):")
    # Displaying the Job_Title and a snippet of Tasks to verify separation
    print(df[['Job_Title', 'Company_Name', 'Job_Search_Term']].head())

    # Save the data with the desired semicolon delimiter
    print("-" * 50)
    print(f"Saving file with new delimiter to: {output_file_path}")

    # Save the DataFrame using the semicolon (;) as the new separator
    df.to_csv(
        output_file_path,
        sep=';',
        index=False,  # Do not write the pandas row index as a column
        encoding='utf-8',

    )

    print(f"✅ File successfully saved with semicolon delimiter.")

except FileNotFoundError:
    print(f"🛑 Error: The file was not found at the path: {input_file_path}")
except Exception as e:
    print(f"🛑 An unexpected error occurred: {e}")