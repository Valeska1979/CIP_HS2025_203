import pandas as pd
import numpy as np
import os

# --- Configuration ---
# Relative path to the raw dataset.
FILE_PATH = '../data/raw/jobs_ch_skills_all.csv'
DELIMITER = ';'

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

# --- Output ---
print(f"Rows with missing Tasks and Skills: {len(df_subset_and)}")








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

