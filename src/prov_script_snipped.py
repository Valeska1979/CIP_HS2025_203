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

# --- CLEANUP (OPTIONAL DELETION) ---

print("-" * 50)
delete_choice = input(f"Do you want to delete the session file '{SESSION_FILE_NAME}'? (y/n): ").strip().lower()

if delete_choice == 'y':
    try:
        os.remove(session_file_path)
        print(f"Successfully deleted session file: '{SESSION_FILE_NAME}'")
    except OSError as e:
        print(f"Error deleting file {SESSION_FILE_NAME}: {e}")
else:
    print(f"Session file '{SESSION_FILE_NAME}' retained.")