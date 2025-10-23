import pandas as pd
from pathlib import Path
import re
import os

# --- CONFIGURATION ---

BASE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BASE_DIR.parent
DATA_DIR = PROJECT_ROOT / "data" / "raw"

MASTER_FILE_NAME = "jobs_ch_skills_all.csv"
MASTER_FILE_PATH = DATA_DIR / MASTER_FILE_NAME

# --- USER INPUT AND DYNAMIC FILE NAMING ---

job_search_term = input("Enter the job title of the session file you want to consolidate (e.g., Data Scientist): ")
safe_job_name = re.sub(r'\s+', '_', job_search_term.strip().lower())
safe_job_name = re.sub(r'[^a-z0-9_]', '', safe_job_name)

SESSION_FILE_NAME = f"jobs_ch_{safe_job_name}_skills.csv"
SESSION_FILE_PATH = DATA_DIR / SESSION_FILE_NAME

# --- CORE CONSOLIDATION LOGIC ---

print("-" * 50)
print(f"Attempting to consolidate data from: {SESSION_FILE_NAME}")
print("-" * 50)

if not SESSION_FILE_PATH.exists():
    print(f"Error: Session file not found at path: {SESSION_FILE_PATH}")
    print(f"Expected location: {SESSION_FILE_PATH.resolve()}")
    exit()

try:
    # Load the session data
    df_session = pd.read_csv(SESSION_FILE_PATH, sep=';')
    records_to_append = len(df_session)

    if records_to_append == 0:
        print("Warning: Session file is empty. No data to consolidate.")
        exit()

    # Determine the starting index for the new data
    master_file_exists = MASTER_FILE_PATH.exists() and MASTER_FILE_PATH.stat().st_size > 0

    if master_file_exists:
        # Load ONLY the 'Job_Index' column from the master file to find the max index
        # This handles the continuous index requirement!
        df_master_index = pd.read_csv(MASTER_FILE_PATH, sep=';', usecols=['Job_Index'])
        start_index = df_master_index['Job_Index'].max() + 1
    else:
        # If master file is new, start indexing at 1
        start_index = 1

    print(f"Starting index for new records will be: {start_index}")

    # Recalculate the Job_Index column in the session data
    df_session['Job_Index'] = range(start_index, start_index + records_to_append)

    # Save the session data to the Master CSV
    df_session.to_csv(MASTER_FILE_PATH,
                      mode='a',
                      header=not master_file_exists,
                      index=False,
                      sep=';')

    print(
        f"SUCCESS! {records_to_append} records from '{SESSION_FILE_NAME}' successfully copied to '{MASTER_FILE_NAME}'.")

except Exception as e:
    print(f"A critical error occurred during consolidation: {e}")
    exit()

# --- CLEANUP (OPTIONAL DELETION) ---

print("-" * 50)
delete_choice = input(f"Do you want to delete the session file '{SESSION_FILE_NAME}'? (y/n): ").strip().lower()

if delete_choice == 'y':
    try:
        os.remove(SESSION_FILE_PATH)
        print(f"Successfully deleted session file: '{SESSION_FILE_NAME}'")
    except OSError as e:
        print(f"Error deleting file {SESSION_FILE_NAME}: {e}")
else:
    print(f"Session file '{SESSION_FILE_NAME}' retained.")

print("-" * 50)
print("Consolidation script finished.")