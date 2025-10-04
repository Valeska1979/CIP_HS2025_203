import pandas as pd
from pathlib import Path

# --- CONFIGURATION (Matching scraper's setup) ---
BASE_DIR = Path(__file__).resolve().parent
# Assumes the script is run from the 'src' directory, going up two levels to find the project root
# Adjust BASE_DIR or DATA_DIR if  script is run from a different location
DATA_DIR = BASE_DIR.parent / "data" / "raw"

FILE_NAME = "jobs_ch_data_science_skills.csv"
FILE_PATH = DATA_DIR / FILE_NAME
# ----------------------------------------------------

# --- DATA LOADING ---
try:
    df = pd.read_csv(FILE_PATH, sep=';')
    print(f"Successfully loaded {len(df)} records from {FILE_NAME}.\n")
except FileNotFoundError:
    print(f"Error: File not found at {FILE_PATH}")
    exit()
except Exception as e:
    print(f"Error loading CSV: {e}")
    exit()

# --- 1. CHECK FOR MISSING VALUES (NaN) ---
print("--- 1. Missing Data (NaN) Check ---")
print(df.isnull().sum())
print("\nAny column with  true missing data (NaN).\n")

# --- 2. CHECK FOR MISSING SCRAPED CONTENT (Tasks and Skills) ---
# We check for the specific string used when extraction failed: "no [...] found on this job ad"

TASKS_MISSING_VALUE = "no tasks found on this job ad"
SKILLS_MISSING_VALUE = "no skills found on this job ad"

# Count jobs with missing Tasks/Skills
jobs_missing_tasks = df[df['Tasks'] == TASKS_MISSING_VALUE]
jobs_missing_skills = df[df['Skills'] == SKILLS_MISSING_VALUE]

print("--- 2. Jobs Missing Scraped Content Check ---")
print(f"Total jobs with no Tasks found: {len(jobs_missing_tasks)}")
print(f"Total jobs with no Skills found: {len(jobs_missing_skills)}")
print("-" * 40)
print(f"Total jobs in file: {len(df)}")
print("-" * 40)

# --- 3. DISPLAY A SAMPLE OF THE MISSING JOBS (Optional) ---
if not jobs_missing_skills.empty:
    print("\n--- Sample of Jobs Missing Skills (First 5) ---")
    # Display Job Title and Company for easy identification
    print(jobs_missing_skills[['Job_Title', 'Company_Name', 'Skills']].head().to_string())

if not jobs_missing_tasks.empty and len(jobs_missing_tasks) != len(df):
    print("\n--- Sample of Jobs Missing Tasks (First 5) ---")
    print(jobs_missing_tasks[['Job_Title', 'Company_Name', 'Tasks']].head().to_string())