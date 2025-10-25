# --- Configuration ---
# Base Directory Setup
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROCESSED_DIR = os.path.join(project_root, 'data', 'processed')
RAW_DIR = os.path.join(project_root, 'data', 'raw')

# File Path Definition
FILE_PATH = os.path.join(RAW_DIR, 'jobs_ch_skills_all.csv') # Input
INTERMEDIATE_FILE_PATH = os.path.join(PROCESSED_DIR, 'jobs_ch_skills_all_cleaned.csv')
FINAL_FILE_PATH = os.path.join(PROCESSED_DIR, 'jobs_ch_skills_all_cleaned_final_V1.csv')

# Data Loading
df = pd.read_csv(FILE_PATH, sep=DELIMITER)
print(f"Data loaded. Total rows: {len(df)}")


os.makedirs(PROCESSED_DIR, exist_ok=True) # Ensure the output directory exists before saving
    df_cleaned_and.to_csv(intermediate_output_path, sep=DELIMITER, index=False) # Save the cleaned DataFrame to the specified path