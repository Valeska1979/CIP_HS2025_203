# ==========================================================
# Data Consolidation and Merging Script
# ==========================================================
# Goal:
#   Safely append a newly scraped session CSV file to the master dataset
#   while maintaining continuous indexing and supporting optional cleanup.
# Key Functionality:
#   - Calculates the next unique 'Job_Index' for seamless record addition.
#   - Appends all new session records to the master CSV for historical tracking.
#   - Provides an option to delete the temporary session file post-merge.
# Author: Stefan Dreyfus
# ==========================================================


import pandas as pd
from pathlib import Path
import re
import os

CSV_DELIMITER = ';'

#Determines the next available unique Job_Index for new records
#by finding the maximum index in the master file and adding 1.
def get_next_job_index(master_file_path: Path) -> int:

    next_job_index = 1

    # Check if the master file exists and has content
    if os.path.exists(master_file_path) and os.path.getsize(master_file_path) > 0:
        try:
            master_df = pd.read_csv(
                master_file_path,
                sep=CSV_DELIMITER,
                usecols=['Job_Index']
            )

            # Ensure the DataFrame is not empty and the column exists
            if not master_df.empty and 'Job_Index' in master_df.columns:
                next_job_index = int(master_df['Job_Index'].max()) + 1

        except pd.errors.EmptyDataError:
            print(f"WARNING: Master file is empty or corrupted: {master_file_path}. Starting index at 1.")
        except Exception as e:
            print(f"ERROR: Failed to read Job_Index from master file. Starting index at 1. Error: {e}")

    return next_job_index

def merge_session_to_master(session_file_path: Path, master_file_path: Path, delete_session: bool = False):

    # --- CORE CONSOLIDATION LOGIC ---
    print("-" * 50)
    print(f"Starting to consolidate data from: {session_file_path}")
    print("-" * 50)

    if not session_file_path.exists():
        print(f"Error: Session file not found at path: {session_file_path}")
        print(f"Expected location: {session_file_path.resolve()}")
        return False

    try:
        # Load the session data
        df_session = pd.read_csv(session_file_path, sep=CSV_DELIMITER)
        records_to_append = len(df_session)

        if records_to_append == 0:
            print("Warning: Session file is empty. No data to consolidate.")
            return False

        # Determine the starting index for the new data
        master_file_exists = master_file_path.exists() and master_file_path.stat().st_size > 0

        # Determine the starting index for the new data using the helper function
        start_index = get_next_job_index(master_file_path)

        print(f"Starting index for new records will be: {start_index}")

        # Recalculate the Job_Index column in the session data
        df_session['Job_Index'] = range(start_index, start_index + records_to_append)

        # Save the session data to the Master CSV
        df_session.to_csv(master_file_path,
                          mode='a',
                          header=not master_file_exists,
                          index=False,
                          sep=CSV_DELIMITER)

        print(
            f"{records_to_append} records from '{session_file_path}' successfully copied to '{master_file_path}'.")

    except Exception as e:
        print(f"A critical error occurred during consolidation: {e}")
        exit()

    # --- Clean up Session File ---
    if delete_session:
        try:
            os.remove(session_file_path)
            print(f"Successfully deleted session file: '{session_file_path}'")
        except OSError as e:
            print(f"Error deleting file {session_file_path}: {e}")
    else:
        print(f"Session file '{session_file_path}' retained (delete_session=False).")

    print("-" * 50)
    print("Consolidation script finished.")
    return True


# --- STANDALONE EXECUTION BLOCK ---
if __name__ == "__main__":
    print("--- RUNNING MERGING SCRIPT IN STANDALONE TEST MODE ---")

    # Relative path definition for this script
    PROJECT_ROOT_TEST = Path(__file__).resolve().parent.parent.parent
    RAW_DATA_DIR_TEST = PROJECT_ROOT_TEST / "data" / "raw"

    # User Input to find the file
    job_search_term = input("Enter the job title of the session file you want to consolidate (e.g., Data Scientist): ")
    safe_job_name = re.sub(r'\s+', '_', job_search_term.strip().lower())
    safe_job_name = re.sub(r'[^a-z0-9_]', '', safe_job_name)

    # Use TEST paths
    TEST_SESSION_FILE_PATH = RAW_DATA_DIR_TEST / f"jobs_ch_{safe_job_name}_skills.csv"
    TEST_MASTER_FILE_PATH = RAW_DATA_DIR_TEST / "jobs_ch_skills_all.csv"

    # User input for deletion preference
    delete_choice = input(
        f"Do you want to delete the session file '{TEST_SESSION_FILE_PATH.name}'? (y/n): ").strip().lower()
    SHOULD_DELETE_TEST = (delete_choice == 'y')

    # Call the main function
    merge_session_to_master(TEST_SESSION_FILE_PATH, TEST_MASTER_FILE_PATH, SHOULD_DELETE_TEST)