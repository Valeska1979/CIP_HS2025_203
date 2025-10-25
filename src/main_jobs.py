import sys
from pathlib import Path
import os
import re

# Import Modules
import jobs_scraping_V1
import csv_merging
import stefan_cleaning_V1
import analysis.analyze_jobs_semantic_clustering

# Definition the Project Root and Standard Paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Defintion all Input / Output Paths
RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"
PROCESSED_DATA_DIR = PROJECT_ROOT / "data" / "processed"
REPORT_DIR = PROJECT_ROOT / "report"

# Ensure directories exist
os.makedirs(RAW_DATA_DIR, exist_ok=True)
os.makedirs(PROCESSED_DATA_DIR, exist_ok=True)
os.makedirs(REPORT_DIR, exist_ok=True)


def run_full_data_pipeline(search_term: str, max_jobs: int, delete_session: bool):
    # Clean the search term to create robust file names
    safe_job_name = re.sub(r'\s+', '_', search_term.strip().lower())
    safe_job_name = re.sub(r'[^a-z0-9_]', '', safe_job_name)

    # Define the specific file paths for the current session
    SESSION_FILE_PATH = RAW_DATA_DIR / f"jobs_ch_{safe_job_name}_skills.csv"
    MASTER_FILE_PATH = RAW_DATA_DIR / "jobs_ch_skills_all.csv"
    INTERMEDIATE_CLEANED_PATH = PROCESSED_DATA_DIR / "jobs_ch_skills_all_intermediate.csv"
    FINAL_CLEANED_PATH = PROCESSED_DATA_DIR / "jobs_ch_skills_all_cleaned_final_V1.csv"
    CLUSTERS_CSV_PATH = PROCESSED_DATA_DIR / "jobs_ch_semantic_clusters_labeled.csv"
    CLUSTERS_PLOT_PATH = REPORT_DIR / "semantic_clusters_umap.png"

    print(f"--- Starting Full Data Pipeline for '{search_term}' (Max: {max_jobs}) ---")

    # --- SCRAPING ---
    try:
        print("\n[1/5] Running Scraper")

        # Call the refactored function, passing all required paths/values
        jobs_scraped = jobs_scraping_V1.scrape_jobs(
            job_search_term=search_term,
            max_jobs_to_scrape=max_jobs,
            save_file_path=SESSION_FILE_PATH,
            master_file_path=MASTER_FILE_PATH
        )
        print(f"Scraping completed. Found {len(jobs_scraped)} new records.")
    except Exception as e:
        print(f"SCRAPING FAILED: {e}");
        sys.exit(1)

    # --- MERGING ---
    try:
        print("\n[2/5] Merging Data")
        success = csv_merging.merge_session_to_master(
            session_file_path=SESSION_FILE_PATH,
            master_file_path=MASTER_FILE_PATH,
            delete_session=delete_session
        )
        if success:
            print("Merging completed successfully.")
        else:
            print("Merging step skipped or failed. Continuing pipeline...")

    except Exception as e:
        print(f"MERGING FAILED: {e}");
        sys.exit(1)

    # --- CLEANING ---
    if os.path.exists(MASTER_FILE_PATH):
        try:
            print("\n[3/5] Cleaning Data")

            cleaned_df = stefan_cleaning_V1.run_data_cleaning(
                input_file_path=MASTER_FILE_PATH,
                intermediate_output_path=INTERMEDIATE_CLEANED_PATH,
                final_output_path=FINAL_CLEANED_PATH
            )

            if cleaned_df is not None:
                print(f"Cleaning completed successfully. Final size: {len(cleaned_df)} records.")
            else:
                print("Cleaning step skipped or failed. Check cleaning script logs.")

        except Exception as e:
            print(f"CLEANING FAILED: {e}");
            sys.exit(1)
    else:
        # Critical failure: Master file (input for cleaning) is missing.
        print("\n[3/5] CLEANING CRITICAL FAILURE: Master file does not exist after merging. Pipeline cannot proceed without the master data file. Exiting.")
        sys.exit(1)

    # --- SEMANTIC CLUSTERING ANALYSIS ---
    # Only run if the FINAL_CLEANED_PATH exists
    if os.path.exists(FINAL_CLEANED_PATH):
        try:
            print("\n[4/5] Running Semantic Clustering Analysis...")

            analysis_success = analysis.analyze_jobs_semantic_clustering.run_semantic_clustering(
                input_file_path=FINAL_CLEANED_PATH,
                output_csv_path=CLUSTERS_CSV_PATH,
                output_plot_path=CLUSTERS_PLOT_PATH
            )

            if analysis_success:
                print("Semantic Clustering completed successfully.")
            else:
                print("Semantic Clustering failed. Check script logs.")
                sys.exit(1)

        except Exception as e:
            print(f"CLUSTERING CRITICAL FAILED: {e}");
            sys.exit(1)
    else:
        print("\n[4/5] Clustering step skipped: Final cleaned data file does not exist. Exiting.")
        sys.exit(1)


if __name__ == "__main__":

    # --- User Input Scraping ---

    # Ask for the job search term
    job_search_term = input("Enter the job title you want to scrape (e.g., Data Scientist): ")

    # Ask for the maximum number of jobs to scrape
    while True:
        try:
            max_jobs_input = input("Enter the maximum number of jobs to scrape (e.g., 50): ")
            MAX_JOBS = int(max_jobs_input)
            if MAX_JOBS <= 0:
                print("Please enter a positive number.")
                continue
            break
        except ValueError:
            print("Invalid input. Please enter a whole number.")


    # --- User Input Deleting Session File ---
    delete_choice = input(
        "Do you want to delete the session CSV file after a successful merge? (y/n): ").strip().lower()
    SHOULD_DELETE_SESSION = (delete_choice == 'y')

    # Call the pipeline runner function with the collected user input
    run_full_data_pipeline(job_search_term, MAX_JOBS, SHOULD_DELETE_SESSION)