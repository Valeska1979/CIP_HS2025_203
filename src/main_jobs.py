# ==========================================================
# Main Data Pipeline Orchestrator
# ==========================================================
# Goal:
#   Execute the end-to-end data pipeline for Data Science job
#   market analysis, from scraping to visualization.
# Workflow Steps:
#   1. Scrape new job data from jobs.ch.
#   2. Merge new data into the master CSV.
#   3. Clean and filter the master dataset.
#   4. Analyze job texts (Tasks).
#   5. Analyze job texts (Skills and Location).
#   6. Perform semantic clustering on cleaned data.
# Execution:
#   Runs interactively, prompting the user for scrape parameters.
# Author: Stefan Dreyfus
# ==========================================================


import sys
from pathlib import Path
import os
import re

# Import Modules
import scraping as jobs_scraping_V1
import cleaning
import analysis
import src.visualization as vis

# Definition the Project Root and Standard Paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Defintion all Input / Output Paths
RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"
PROCESSED_DATA_DIR = PROJECT_ROOT / "data" / "processed"
REPORT_DIR = PROJECT_ROOT / "report"
ANALYSIS_DATA_DIR = PROJECT_ROOT / "data" / "analysis"
DATA_VIS_DIR = PROJECT_ROOT / "data" / "visualization"

# Ensure directories exist
os.makedirs(RAW_DATA_DIR, exist_ok=True)
os.makedirs(PROCESSED_DATA_DIR, exist_ok=True)
os.makedirs(REPORT_DIR, exist_ok=True)
os.makedirs(ANALYSIS_DATA_DIR, exist_ok=True)
os.makedirs(DATA_VIS_DIR, exist_ok=True)


def run_full_data_pipeline(search_term: str, max_jobs: int, delete_session: bool):
    # Clean the search term to create robust file names
    safe_job_name = re.sub(r'\s+', '_', search_term.strip().lower())
    safe_job_name = re.sub(r'[^a-z0-9_]', '', safe_job_name)

    # Define the specific file paths for the current session
    SESSION_FILE_PATH = RAW_DATA_DIR / f"jobs_ch_{safe_job_name}_skills.csv"
    MASTER_FILE_PATH = RAW_DATA_DIR / "jobs_ch_skills_all.csv"
    INTERMEDIATE_CLEANED_PATH = PROCESSED_DATA_DIR / "jobs_ch_skills_all_intermediate.csv"
    FINAL_CLEANED_PATH = PROCESSED_DATA_DIR / "jobs_ch_skills_all_cleaned_final_V1.csv"
    CLUSTERS_CSV_PATH = ANALYSIS_DATA_DIR / "jobs_ch_semantic_clusters_labeled.csv"
    CLUSTERS_PLOT_PATH = REPORT_DIR / "figures" / "cluster_plot.png"
    JOB_COUNTS_PER_LOCATION_PATH = DATA_VIS_DIR / "jobs_ch_location_counts_1.csv"
    JOB_COUNTS_PER_CANTON_PATH = DATA_VIS_DIR / "Job_per_canton.csv"
    CANTON_MAP_OUTPUT_PATH = REPORT_DIR / "figures" / "jobs_maps_switzerland.png"
    SINGLE_SKILL_CSV_PATH = ANALYSIS_DATA_DIR / "jobs_ch_single_skills_analysis.csv"
    SINGLE_SKILL_PLOT_PATH = REPORT_DIR / "figures" / "required_single_skills.png"
    # ------------------------------------------


    # INPUT PATH for Skills Analysis
    SKILLS_INPUT_PATH = FINAL_CLEANED_PATH

    # INPUT PATH for Tasks Analysis
    TASKS_INPUT_PATH = FINAL_CLEANED_PATH

    print(f"--- Starting Full Data Pipeline for '{search_term}' (Max: {max_jobs}) ---")

    # --- SCRAPING ---
    try:
        print("\n[1/6] Running Scraper")

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
        print("\n[2/6] Merging Data")
        success = jobs_scraping_V1.merge_session_to_master(
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
            print("\n[3/6] Cleaning Data")

            cleaned_df = cleaning.run_data_cleaning(
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
        print("\n[3/6] CLEANING CRITICAL FAILURE: Master file does not exist after merging. Pipeline cannot proceed without the master data file. Exiting.")
        sys.exit(1)

    # --- TASKS ANALYSIS ---
    if os.path.exists(TASKS_INPUT_PATH):
        try:
            print("\n[4/6] Running Tasks Analysis")

            task_analysis_success = analysis.run_task_analysis(
                input_file_path=TASKS_INPUT_PATH,
                output_dir_path=ANALYSIS_DATA_DIR
            )

            if task_analysis_success:
                print("Tasks Analysis completed successfully.")
            else:
                print("Tasks Analysis failed. Check script logs.")
                sys.exit(1)

        except Exception as e:
            print(f"TASKS ANALYSIS CRITICAL FAILED: {e}");
            sys.exit(1)
    else:
        print("\n[4/6] Tasks Analysis step skipped: Final cleaned data file does not exist. Exiting.")
        sys.exit(1)


    # --- SKILLS AND LOCATION ANALYSIS ---

    if os.path.exists(SKILLS_INPUT_PATH):
        try:
            print("\n[5/6] Running Skills and Location Analysis")

            analysis_success = analysis.run_skills_analysis(
                input_file_path=SKILLS_INPUT_PATH,
                output_dir_path=ANALYSIS_DATA_DIR
            )

            if analysis_success:
                print("Skills and Location Analysis completed successfully.")
            else:
                print("Skills and Location Analysis failed. Check script logs.")
                sys.exit(1)

        except Exception as e:
            print(f"SKILLS ANALYSIS CRITICAL FAILED: {e}");
            sys.exit(1)
    else:
        print("\n[5/6] Skills Analysis step skipped: Clustered data file does not exist. Exiting.")
        sys.exit(1)

    # --- SEMANTIC CLUSTERING ANALYSIS ---
    # Only run if the FINAL_CLEANED_PATH exists
    if os.path.exists(FINAL_CLEANED_PATH):
        try:
            print("\n[6/6] Running Semantic Clustering Analysis")

            analysis_success = analysis.run_semantic_clustering(
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
        print("\n[6/6] Clustering step skipped: Final cleaned data file does not exist. Exiting.")
        sys.exit(1)

    # --- CANTON MAP VISUALIZATION ---
    if os.path.exists(JOB_COUNTS_PER_LOCATION_PATH):
        try:
            print("\n[7/6] Running Canton Map Visualization")

            map_success = vis.create_canton_map_visualization(
                job_counts_input_path=JOB_COUNTS_PER_LOCATION_PATH,
                report_output_path=CANTON_MAP_OUTPUT_PATH,
                job_per_canton_output_path=JOB_COUNTS_PER_CANTON_PATH
            )

            if map_success:
                print("Canton Map Visualization completed successfully.")
            else:
                print("Canton Map Visualization failed. Check script logs.")
                sys.exit(1)

        except Exception as e:
            print(f"MAP VISUALIZATION CRITICAL FAILED: {e}");
            sys.exit(1)
    else:
        print(
            f"\n[7/6] Map Visualization skipped: Input file not found at {JOB_COUNTS_PER_LOCATION_PATH}. Exiting.")
        sys.exit(1)

    # --- SINGLE SKILL VISUALIZATION ---
    if os.path.exists(SINGLE_SKILL_CSV_PATH):
        try:
            print("\n[8/6] Running Single Skill Visualization")

            vis_success = vis.create_single_skill_visualization(
                input_file_path=SINGLE_SKILL_CSV_PATH,
                output_file_path=SINGLE_SKILL_PLOT_PATH
            )

            if vis_success:
                print("Single Skill Visualization completed successfully.")
            else:
                print("Single Skill Visualization failed. Check script logs.")
                sys.exit(1)

        except Exception as e:
            print(f"SINGLE SKILL VISUALIZATION CRITICAL FAILED: {e}");
            sys.exit(1)
    else:
        print(
            f"\n[8/6] Single Skill Visualization skipped: Input file not found at {SINGLE_SKILL_CSV_PATH}. Exiting.")
        sys.exit(1)

# --- FINAL STATUS ---
    print("\n--- Pipeline Execution Complete! (All 6 steps successfully executed) --- ")

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