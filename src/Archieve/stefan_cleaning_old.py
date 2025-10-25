import pandas as pd
import os

# --- Configuration ---
# Relative path to the raw dataset.
FILE_PATH = '../../data/raw/jobs_ch_skills_all.csv'
DELIMITER = ';'

#Relative path for cleaned dataset
PROCESSED_DIR = '../../data/processed/'
OUTPUT_CLEANED_DATASET = 'jobs_ch_skills_all_intermediate.csv'
CLEANED_DATASET_FILE_PATH = os.path.join(PROCESSED_DIR, OUTPUT_CLEANED_DATASET)

# Define the specific strings to filter for, indicating missing data
MISSING_TASK_STRING = 'no tasks found on this job ad'
MISSING_SKILL_STRING = 'no skills found on this job ad'

# --- Data Loading ---
df = pd.read_csv(FILE_PATH, sep=DELIMITER)
print(f"Data loaded. Total rows: {len(df)}")



# --- Filtering No Tasks AND No Skills ---
# 1. Create a boolean Series for rows where the Tasks and Skills column matches the missing string.
missing_tasks_mask = (df["Tasks"] == MISSING_TASK_STRING)
missing_skills_mask = (df["Skills"]) == MISSING_SKILL_STRING

#2. Combine the masks using the AND (&) operator to select rows where both condition is True.
combined_filter_and = missing_tasks_mask & missing_skills_mask

#3. Applying the filter and creating a subset
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

#Small test if the dataset df_cleaned_and does not have rows with both missing Tasks AND Skills
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
    print("The exclusion was successful.")
else:
    print(f"WARNING: The 'df_cleaned_and' DataFrame contains **{rows_to_check_count}** rows that should have been excluded.")

print("-" * 30)


# --- Filtering No Tasks ---
df_cleaned = df_cleaned_and #reasigning variable for better understanding

#Applying the filter and inspection

df_subset_notasks = df_cleaned[(df_cleaned["Tasks"] == MISSING_TASK_STRING)]

print(f"Rows with misssing Tasks in the cleaned dataset: {len(df_subset_notasks)}")

"No rows with only missing Tasks in the cleaned dataset"


# --- Filtering No Skills ---

#1. Applying the filter and inspection

df_subset_noskills = df_cleaned[(df_cleaned["Skills"] == MISSING_SKILL_STRING)]

print(f"Rows with misssing Skills in the cleaned dataset: {len(df_subset_noskills)}")

"df_subset_noskills was inspected in View mode. Jobs unrelated to Data Science were identified and removed. It was also checked whether any skills appeared in the Tasks column instead of Skills — if so, they were kept as-is. After review, jobs were removed from the cleaned dataset based on their Job Index."


#Exclusion of Specific Jobs by Job_Index
# The list of Job_Index values to be excluded
JOB_INDICES_TO_EXCLUDE = [
    24, 43, 49, 58, 62, 64, 77, 80, 82, 90, 91, 95, 103, 104,
    116, 117, 119, 126, 132, 146, 148, 167, 182, 185, 186, 189,
    202, 210, 220, 221, 224, 237, 241, 243, 249, 250, 259, 260,
    274, 276, 283, 287, 290, 293, 294, 298, 308, 310, 327, 342,
    348, 351
]

# Create a boolean mask: True for rows where Job_Index is IN the exclusion list
exclusion_mask = df_cleaned['Job_Index'].isin(JOB_INDICES_TO_EXCLUDE)

# Apply the filter to keep only the rows where the mask is False (i.e., NOT in the exclusion list)
df_cleaned = df_cleaned[~exclusion_mask]

print("-" * 30)
print(f"Total rows in cleaned data: {len(df_cleaned)}")
print("-" * 30)


# --- Saving the Cleaned Dataset ---

# Overwrite CSV with the final cleaned dataset
FINAL_CLEANED_DATASET = 'jobs_ch_skills_all_final_cleaned.csv'
FINAL_CLEANED_DATASET_FILE_PATH = os.path.join(PROCESSED_DIR, FINAL_CLEANED_DATASET)

# Saving the cleaned DataFrame to the specified path
df_cleaned.to_csv(FINAL_CLEANED_DATASET_FILE_PATH, sep=DELIMITER, index=False)

print(f"\nFinal cleaned dataset saved to: {FINAL_CLEANED_DATASET_FILE_PATH}")


# --- Filtering Job Titles---

"As the next step, job titles unrelated to Data Science were removed. Jobs were also excluded where the listed skills had on a first glimpse no clear connection to Data Science or our degree — e.g., technical trades, engineering, life sciences, or PhD-level roles."

#Exclusion of Specific Jobs by Job_Index
# The list of Job_Index values to be included
JOB_INDICES_TO_INCLUDE = [
    1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 15, 16, 18, 19, 20, 25, 27, 28, 29, 30,
    31, 32, 33, 34, 35, 36, 37, 38, 40, 44, 48, 50, 53, 65, 359, 360, 361, 365,
    367, 369, 371, 373, 375, 376, 381, 383, 384, 386, 387, 388, 391, 395, 398,
    399, 403, 302, 303, 304, 305, 306, 312, 313, 314, 316, 319, 320, 322, 323,
    325, 331, 332, 338, 339, 340, 341, 343, 344, 346, 350, 352, 357, 172, 174,
    83, 84, 92, 93, 196, 200, 226, 133, 135, 137, 150, 248, 156, 288, 301, 201,
    203, 204, 205, 206, 309, 207, 208, 209, 211, 212, 213, 214, 215, 321, 216,
    217, 324, 218, 326, 328, 219, 222, 223, 225, 334, 227, 228, 229, 230, 231,
    233, 234, 235, 236, 238, 239, 240, 242, 244, 246, 358, 251, 263, 374, 268,
    269, 270, 271, 272, 273, 277, 278, 279, 280, 281, 282, 284, 397, 285, 289,
    291, 292, 296, 297, 299, 300, 408
]

# Create a boolean mask: True for rows where Job_Index is IN the including list
inclusion_mask = df_cleaned['Job_Index'].isin(JOB_INDICES_TO_INCLUDE)

# Apply the filter to keep only the rows where the mask is TRUE and create a new subset
df_cleaned_final = df_cleaned[inclusion_mask].copy()

print("-" * 30)
print(f"Total rows in cleaned data: {len(df_cleaned_final)}")
print("-" * 30)


# --- Saving the Cleaned Dataset as a new CSV---

# Build the path relative to the project root
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
output_path = os.path.join(project_root, "data", "processed", "jobs_ch_skills_all_cleaned_final_V1.csv")

# Create the directory if it doesn't exist
os.makedirs(os.path.dirname(output_path), exist_ok=True)

# Save to CSV (without the index column)
df_cleaned_final.to_csv(output_path, index=False)

print(f"File saved successfully at: {output_path}")

