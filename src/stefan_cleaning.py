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











# --- Filtering No Tasks OR No Skills ---
# 1. Create a boolean Series for rows where the 'Tasks' and 'Skills' column matches the missing string.
missing_tasks_mask = (df["Tasks"] == MISSING_TASK_STRING)
missing_skills_mask = (df["Skills"]) == MISSING_SKILL_STRING

#2. Combine the masks using the OR operator (|) to select rows where *either* condition is True.
combined_filter = missing_tasks_mask | missing_skills_mask

#4. Applying the filter and creating a subset

df_subset = df[combined_filter].copy()

# --- Output ---
print("\n--- Filtered Subset Summary ---")
print(f"Rows with missing Tasks: {missing_tasks_mask.sum()}, {round(missing_tasks_mask.sum() / len(df)*100, 2)}% of the dataset ")
print(f"Rows with missing Skills: {missing_skills_mask.sum()}, {round(missing_skills_mask.sum() / len(df)*100, 2)}% of the dataset")

"22% of the 'Skills' seems to miss. However, this is not a big issue because 'Skills' could also be in the 'Tasks' column. We proceede further with cleaning"

