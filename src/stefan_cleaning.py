import pandas as pd
import numpy as np
import os

# --- Configuration ---
# Relative path to the raw dataset.
FILE_PATH = '../data/raw/jobs_ch_skills_all.csv'
DELIMITER = ';'

#Relative path for cleaned dataset
PROCESSED_DIR = '../data/processed/'
OUTPUT_CLEANED_DATASET = 'jobs_ch_skills_all_cleaned.csv'
CLEANED_DATASET_FILE_PATH = os.path.join(PROCESSED_DIR, OUTPUT_CLEANED_DATASET)

# Define the specific strings to filter for, indicating missing data
MISSING_TASK_STRING = 'no tasks found on this job ad'
MISSING_SKILL_STRING = 'no skills found on this job ad'

# --- Data Loading ---
df = pd.read_csv(FILE_PATH, sep=DELIMITER)
print(f"Data loaded successfully. Total rows: {len(df)}")



# --- Filtering No Tasks AND No Skills ---
# 1. Create a boolean Series for rows where the 'Tasks' and 'Skills' column matches the missing string.
missing_tasks_mask = (df["Tasks"] == MISSING_TASK_STRING)
missing_skills_mask = (df["Skills"]) == MISSING_SKILL_STRING

#2. Combine the masks using the AND (&) operator to select rows where both condition is True.
combined_filter_and = missing_tasks_mask & missing_skills_mask

#4. Applying the filter and creating a subset

df_subset_and = df[combined_filter_and].copy()

print(f"Rows with missing Tasks and Skills: {len(df_subset_and)}")

#Excluding rows where there are no tasks AND no skills

df_cleaned_and = df[~combined_filter_and].copy()

rows_excluded = len(df) - len(df_cleaned_and)
print(f"Total rows in original data: {len(df)}")
print(f"Rows excluded (Missing Tasks AND Missing Skills): {rows_excluded}")
print(f"Total rows in cleaned data: {len(df_cleaned_and)}")

"The filter shows most of the jobs having both no Tasks and no Skills are jobs which are not relevant for us because they are not Data Science related jobs. So they can be excluded from the dataset"

#Creating a new CSV with the cleaned dataset
os.makedirs(PROCESSED_DIR, exist_ok=True) # Ensure the output directory exists before saving

df_cleaned_and.to_csv(CLEANED_DATASET_FILE_PATH, sep=DELIMITER, index=False) # Save the cleaned DataFrame to the specified path

#Small test if the dataset df_cleaned_and doesnt have rows with both missing Tasks AND Skills
# 1. Create a boolean Series for rows in the cleaned data that still match the exclusion criteria.
# Checking if the exclusion condition is met in the cleaned dataframe.
verification_tasks_mask = (df_cleaned_and["Tasks"] == MISSING_TASK_STRING)
verification_skills_mask = (df_cleaned_and["Skills"] == MISSING_SKILL_STRING)

# 2. Combine the masks using the AND (&) operator to find any rows matching the exclusion criteria.
rows_to_check_mask = verification_tasks_mask & verification_skills_mask

# 3. Count the rows that should not be there.
rows_to_check_count = len(df_cleaned_and[rows_to_check_mask])

# 4. Output the result
print("-" * 30)
print("--- Verification Check ---")

if rows_to_check_count == 0:
    print(f"SUCCESS: The 'df_cleaned_and' DataFrame contains **{rows_to_check_count}** rows with both missing Tasks AND missing Skills.")
    print("The exclusion was successful, as expected.")
else:
    print(f"WARNING: The 'df_cleaned_and' DataFrame unexpectedly contains **{rows_to_check_count}** rows that should have been excluded.")

print("-" * 30)


# --- Filtering No Tasks ---
df_cleaned = df_cleaned_and #reasigning variable for better understanding

#Applying the filter and inspection

df_subset_notasks = df_cleaned[(df_cleaned["Tasks"] == MISSING_TASK_STRING)]

print(f"Rows with misssing Tasks in the cleaned dataset: {len(df_subset_notasks)}")



#Filtering No Skills ---

#1. Applying the filter and inspection

df_subset_noskills = df_cleaned[(df_cleaned["Skills"] == MISSING_SKILL_STRING)]

print(f"Rows with misssing Tasks in the cleaned dataset: {len(df_subset_noskills)}")