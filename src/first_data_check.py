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


    ######################################

    import pandas as pd
    from pathlib import Path
    import os

    # --- CONFIGURATION ---
    # Using the absolute path provided in the initial query for reliability.
    # We convert the raw string path to a Path object for better cross-platform handling.
    FILE_PATH = Path(r"C:\Users\stefa\Pycharm_CIP_Jobs_Project_Github\data\raw\jobs_ch_skills_all.csv")
    CSV_SEPARATOR = ';'

    # Define the specific string values used by the scraper when content was not found
    TASKS_MISSING_VALUE = "no tasks found on this job ad"
    SKILLS_MISSING_VALUE = "no skills found on this job ad"
    # ----------------------------------------------------

    # --- DATA LOADING ---
    df = None
    try:
        # Use pd.read_csv, specifying the semicolon separator
        df = pd.read_csv(FILE_PATH, sep=CSV_SEPARATOR)

        print(f"Successfully loaded data from: {FILE_PATH.name}")
        print(f"DataFrame Shape (Rows, Columns): {df.shape}")

    except FileNotFoundError:
        print(f"ERROR: File not found at the path: {FILE_PATH}")
        # Exit gracefully if the file cannot be found
        exit()
    except Exception as e:
        print(f"An unexpected error occurred during file loading: {e}")
        # Exit gracefully if loading fails for other reasons
        exit()

    # If loading was successful, proceed with data validation and initial analysis
    if df is not None:
        # --- 1. CHECK FOR MISSING VALUES (NaN) ---
        # This checks for true nulls (NaN) in the DataFrame
        print("\n" + "=" * 50)
        print("--- 1. Missing Data (NaN) Check (True Nulls) ---")
        print("Counts of NaN values per column:")
        print(df.isnull().sum())

        # --- 2. CHECK FOR MISSING SCRAPED CONTENT (Tasks and Skills) ---
        # This checks for the specific placeholder strings left by the scraping process
        jobs_missing_tasks = df[df['Tasks'] == TASKS_MISSING_VALUE]
        jobs_missing_skills = df[df['Skills'] == SKILLS_MISSING_VALUE]

        total_jobs = len(df)

        print("\n" + "=" * 50)
        print("--- 2. Jobs Missing Scraped Content Check (Placeholder Strings) ---")
        print(f"Total jobs in file: {total_jobs}")
        print(f"Jobs with no Tasks found: {len(jobs_missing_tasks)} ({len(jobs_missing_tasks) / total_jobs:.2%})")
        print(f"Jobs with no Skills found: {len(jobs_missing_skills)} ({len(jobs_missing_skills) / total_jobs:.2%})")

        # --- 3. DISPLAY A SAMPLE OF THE MISSING JOBS ---
        print("\n" + "=" * 50)
        print("--- 3. Data Samples ---")

        # Display the first 5 rows to verify the overall structure
        print("\n--- General Data Sample (First 5 Rows) ---")
        print(df.head().to_string())

        if not jobs_missing_skills.empty:
            print("\n--- Sample of Jobs Missing Skills (First 3) ---")
            # Display relevant columns for jobs that failed to extract skills
            print(jobs_missing_skills[['Job_Title', 'Company_Name', 'Skills']].head(3).to_string())

        if not jobs_missing_tasks.empty:
            print("\n--- Sample of Jobs Missing Tasks (First 3) ---")
            # Display relevant columns for jobs that failed to extract tasks
            print(jobs_missing_tasks[['Job_Title', 'Company_Name', 'Tasks']].head(3).to_string())

        print("\n" + "=" * 50)
        print("Data loading and initial validation complete.")
