# ==========================================================
# Data Cleaning and Refinement Utility
# ==========================================================
# Goal:
#   Clean and filter the raw jobs.ch dataset to ensure only high-quality,
#   Data Science-relevant records remain for subsequent analysis.
# Key Functionality:
#   - Excludes records missing both Tasks AND Skills descriptions.
#   - Refines data quality by excluding specific, non-relevant jobs based on an indexed inspection list.
#   - Filters data using an extensive keyword list across Title, Tasks, and Skills
#     to eliminate non-Data Science roles (e.g., Legal, HR, Logistics).
# Author: Stefan Dreyfus
# ==========================================================


import pandas as pd
import os
import re
from pathlib import Path
import sys


# Define the delimiter used for all CSV operations
CSV_DELIMITER = ';'
def run_data_cleaning(input_file_path: Path, intermediate_output_path: Path, final_output_path: Path):

    # --- Configuration ---
    # Data Loading
    df = pd.read_csv(input_file_path, sep=';')




    # --- Filtering No Tasks AND No Skills ---

    # Define the specific strings to filter for, indicating missing data
    MISSING_TASK_STRING = 'no tasks found on this job ad'
    MISSING_SKILL_STRING = 'no skills found on this job ad'

    # Create a boolean Series for rows where the Tasks and Skills column matches the missing string.
    missing_tasks_mask = (df["Tasks"] == MISSING_TASK_STRING)
    missing_skills_mask = (df["Skills"]) == MISSING_SKILL_STRING

    # Combine the masks using the AND (&) operator to select rows where both condition is True.
    combined_filter_and = missing_tasks_mask & missing_skills_mask

    # Applying the filter and creating a subset
    df_subset_and = df[combined_filter_and].copy()

    #Excluding rows where there are no tasks AND no skills
    df_cleaned_and = df[~combined_filter_and].copy()

    # Validation output
    rows_excluded = len(df) - len(df_cleaned_and)
    print(f"Total rows in original data: {len(df)}")
    print(f"Rows excluded (Missing Tasks AND Missing Skills): {rows_excluded}")
    print(f"Total rows in cleaned data: {len(df_cleaned_and)}")

    "The filter shows most of the jobs having both no Tasks and no Skills are jobs which are not relevant for us because they are not Data Science related jobs. So they can be excluded from the dataset"

    # Creating an intermediate CSV with the cleaned dataset for inspection and debugging.
    try:
        os.makedirs(intermediate_output_path.parent, exist_ok=True)
        df_cleaned_and.to_csv(intermediate_output_path, sep=CSV_DELIMITER, index=False)
        print(f"Intermediate file saved successfully at: {intermediate_output_path}")
    except Exception as e:
        print(f"WARNING: Intermediate save failed: {e}")

    # Small test if the dataset df_cleaned_and does not have rows with both missing Tasks AND Skills
    # Create a boolean Series for rows in the cleaned data that still match the exclusion criteria. Checking if the exclusion condition is met in the cleaned dataframe.
    verification_tasks_mask = (df_cleaned_and["Tasks"] == MISSING_TASK_STRING)
    verification_skills_mask = (df_cleaned_and["Skills"] == MISSING_SKILL_STRING)

    # Combine the masks using the AND (&) operator to find any rows matching the exclusion criteria.
    rows_to_check_mask = verification_tasks_mask & verification_skills_mask

    # Count the rows that should not be there.
    rows_to_check_count = len(df_cleaned_and[rows_to_check_mask])

    # 4. Output the result
    print("-" * 30)
    print("--- Verification Check ---")

    if rows_to_check_count == 0:
        print(f"SUCCESS: The 'df_cleaned_and' DataFrame contains **{rows_to_check_count}** rows with both missing Tasks AND missing Skills.")
        print("The exclusion was successful.")
    else:
        print(f"WARNING: The 'df_cleaned_and' DataFrame contains **{rows_to_check_count}** rows that should have been excluded.")

    print("-" * 30)


    # --- Filtering No Tasks ---
    # Reasigning variable for better understanding
    df_cleaned = df_cleaned_and

    #Applying the filter and inspection
    df_subset_notasks = df_cleaned[(df_cleaned["Tasks"] == MISSING_TASK_STRING)]

    print(f"Rows with misssing Tasks in the cleaned dataset: {len(df_subset_notasks)}")

    "No rows with only missing Tasks in the cleaned dataset"


    # --- Filtering No Skills ---

    # Filtering for rows with No Skills
    df_subset_noskills = df_cleaned[(df_cleaned["Skills"] == MISSING_SKILL_STRING)]

    print(f"Rows with misssing Skills in the cleaned dataset: {len(df_subset_noskills)}")

    "df_subset_noskills was inspected in View mode. Jobs unrelated to Data Science were identified and removed. It was also checked whether any skills appeared in the Tasks column instead of Skills — if so, they were kept as-is. After review, jobs were removed from the cleaned dataset based on their Job Index."

    rows_before_index_exclusion = len(df_cleaned)

    #Exclusion of Specific Jobs by Job_Index
    JOB_INDICES_TO_EXCLUDE = [
        4, 14, 17, 23, 24, 26, 39, 43, 45, 46, 47, 49, 51, 52,
        54, 57, 58, 62, 63, 64, 66, 77, 80, 82, 90, 91, 95, 100,
        101, 102, 103, 104, 105, 106, 107, 108, 110, 113, 114, 115, 116, 117,
        118, 119, 120, 122, 125, 126, 127, 128, 129, 132, 134, 138, 139, 146,
        148, 152, 154, 155, 157, 158, 159, 160, 161, 163, 166, 167, 168, 169,
        170, 171, 173, 177, 178, 182, 185, 186, 188, 189, 190, 191, 193, 194,
        195, 198, 202, 210, 220, 221, 224, 237, 241, 243, 245, 247, 249, 250,
        252, 253, 254, 255, 256, 259, 260, 261, 262, 264, 265, 266, 267, 274,
        276, 283, 287, 290, 293, 294, 298, 308, 310, 327, 342, 348, 351, 378,
        379, 382, 385, 392, 394, 396, 400, 401
    ]

    # Create a boolean mask: True for rows where Job_Index is IN the exclusion list
    exclusion_mask = df_cleaned['Job_Index'].isin(JOB_INDICES_TO_EXCLUDE)

    # Apply the filter to keep only the rows where the mask is False (i.e., NOT in the exclusion list)
    df_cleaned = df_cleaned[~exclusion_mask]

    rows_excluded_by_index = rows_before_index_exclusion - len(df_cleaned)
    print("-" * 30)
    print(f"Data refinement: {rows_before_index_exclusion} records processed; {rows_excluded_by_index} jobs removed.")
    print("-" * 30)

     # Filtering by Keywords
    "As the further step, a keyword-based exclusion filter was applied across the job Title, Tasks, and Skills columns to remove roles that clearly fell outside the scope of Data Science, such as those explicitly mentioning Lager, Recht, or Chemie. The keywords were indentified meanwhile going through the data set"

    # Define the keywords for exclusion. Keywords will be searched in 'Title', 'Tasks', and 'Skills' columns.
    EXCLUSION_KEYWORDS = [
        #ACADEMIC / HIGHLY SPECIALIZED SCIENCE
        'PH\.D',
        'Doktor',
        'Dozent',
        'Chemie',
        'Biologie',
        'Laborant',
        'Food process',
        'Food engineering',
        #SOCIAL SCIENCES / HUMANITIES / LEGAL
        r'\bRecht\b',
        'Psychologie',
        'Sozialwissenschaften',
        'Geisteswissenschaften',
        #MEDICAL / HEALTHCARE / PHARMACEUTICAL
        r'\bMedizin\b',
        'Infirmières',
        'Infirmier',
        'Pflegeexpert',
        #TRADES / MANUAL / ENGINEERING / LOGISTICS
        'Montage',
        'Monteur',
        'Servicetechniker',
        'Technicien',
        'Mechanical',
        'Manufacturing',
        'Bauingenieur',
        'Lager',
        #BUSINESS SUPPORT / ADMIN / FINANCE
        'HR-Manager',
        'Treuhand',
        'Buchhaltung',

        # Add more keywords here as needed, e.g., 'Engineering', 'Biotech'
    ]

    # Columns to check for the exclusion keywords
    columns_to_check = ['Job_Title', 'Tasks', 'Skills']

    # Build the case-insensitive regex pattern. Escape special characters in keywords (like '.' in 'PH.D') and join them with an OR operator '|'
    regex_pattern = '|'.join([re.escape(k) for k in EXCLUSION_KEYWORDS])

    # Flag for case-insensitivity:
    regex_pattern_with_flags = f'(?i){regex_pattern}'

    # Create a combined boolean exclusion mask
    # Initializing the mask to all False
    exclusion_mask_keywords = pd.Series([False] * len(df_cleaned), index=df_cleaned.index)

    # Iterate over the columns and update the exclusion mask using the logical OR operator
    for col in columns_to_check:
        #Calculate the mask for the current column
        col_mask = df_cleaned[col].astype(str).str.contains(
            regex_pattern_with_flags,
            na=False,
            regex=True
        )
        # The job is excluded if it matches the pattern in ANY of the columns
        exclusion_mask_keywords = exclusion_mask_keywords | col_mask

    # Apply the filter. Keep only the rows where the mask is False
    df_cleaned_final = df_cleaned[~exclusion_mask_keywords].copy()

    # Validation output
    rows_excluded_by_keyword = len(df_cleaned) - len(df_cleaned_final)

    print("-" * 30)
    print(f"Keywords used for exclusion: {', '.join(EXCLUSION_KEYWORDS)}")
    print(f"Total rows before keyword filter: {len(df_cleaned)}")
    print(f"Rows excluded by keyword filter: {rows_excluded_by_keyword}")
    print(f"Total rows in cleaned data: {len(df_cleaned_final)}")
    print("-" * 30)


    # --- CREATING FINAL CSV WITH THE CLEANED DATASET ---
    os.makedirs(os.path.dirname(final_output_path), exist_ok=True)

    df_cleaned_final.to_csv(final_output_path, index=False, sep=CSV_DELIMITER) # Save to CSV (without the index column)

    print(f"File saved successfully at: {final_output_path}")

    return df_cleaned_final

# --- STANDALONE EXECUTION BLOCK ---
if __name__ == "__main__":
    print("--- RUNNING CLEANING SCRIPT IN STANDALONE TEST MODE ---")

    # Define paths relative to this script
    PROJECT_ROOT_TEST = Path(__file__).resolve().parent.parent
    RAW_DATA_DIR_TEST = PROJECT_ROOT_TEST / "data" / "raw"
    PROCESSED_DATA_DIR_TEST = PROJECT_ROOT_TEST / "data" / "processed"

    TEST_INPUT_PATH = RAW_DATA_DIR_TEST / "jobs_ch_skills_all.csv"
    TEST_INTERMEDIATE_PATH = PROCESSED_DATA_DIR_TEST / "jobs_ch_skills_all_intermediate.csv"
    TEST_OUTPUT_PATH = PROCESSED_DATA_DIR_TEST / "jobs_ch_skills_all_cleaned_final_V1.csv"

    # Run the cleaning
    cleaned_df = run_data_cleaning(TEST_INPUT_PATH, TEST_INTERMEDIATE_PATH, TEST_OUTPUT_PATH)

    if cleaned_df is not None:
        print(f"Standalone run complete. Final DataFrame size: {len(cleaned_df)}")
    else:
        print("Standalone run failed.")