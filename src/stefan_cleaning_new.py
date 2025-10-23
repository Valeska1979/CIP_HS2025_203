import pandas as pd
import os
import re

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

#Filtering for rows with No Skills

df_subset_noskills = df_cleaned[(df_cleaned["Skills"] == MISSING_SKILL_STRING)]

print(f"Rows with misssing Skills in the cleaned dataset: {len(df_subset_noskills)}")

"df_subset_noskills was inspected in View mode. Jobs unrelated to Data Science were identified and removed. It was also checked whether any skills appeared in the Tasks column instead of Skills — if so, they were kept as-is. After review, jobs were removed from the cleaned dataset based on their Job Index."


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

print("-" * 30)
print(f"Total rows in cleaned data after exclusion of specific jobs by Job_Index: {len(df_cleaned)}")


# --- Filtering by Keywords---
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

# --- 1. Build the case-insensitive regex pattern ---
# Escape special characters in keywords (like '.' in 'PH.D') and join them with an OR operator '|'
regex_pattern = '|'.join([re.escape(k) for k in EXCLUSION_KEYWORDS])
# Flag for case-insensitivity:
regex_pattern_with_flags = f'(?i){regex_pattern}'

# --- 2. Create a combined boolean exclusion mask ---
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

# --- 3. Apply the filter ---
# Keep only the rows where the mask is False
df_cleaned_final = df_cleaned[~exclusion_mask_keywords].copy()

rows_excluded_by_keyword = len(df_cleaned) - len(df_cleaned_final)

print(f"Keywords used for exclusion: {', '.join(EXCLUSION_KEYWORDS)}")
print(f"Total rows before keyword filter: {len(df_cleaned)}")
print(f"Rows excluded by keyword filter: {rows_excluded_by_keyword}")
print(f"Total rows in cleaned data: {len(df_cleaned_final)}")
print("-" * 30)



# --- Saving the Cleaned Dataset as final CSV---

# Build the path relative to the project root
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
output_path = os.path.join(project_root, "data", "processed", "jobs_ch_skills_all_cleaned_final_V1.csv")

# Create the directory if it doesn't exist
os.makedirs(os.path.dirname(output_path), exist_ok=True)

# Save to CSV (without the index column)
df_cleaned_final.to_csv(output_path, index=False)

print(f"File saved successfully at: {output_path}")

