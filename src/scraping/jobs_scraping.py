# ==========================================================
# Jobs.ch Web Scraper and Data Collection Utility
# ==========================================================
# Goal:
#   Automate the extraction of structured job advertisement data
#   (Title, Company, Location, Tasks, and Skills) from jobs.ch.
# Key Functionality:
#   - Utilizes Selenium to execute search, handle navigation, and extract ad details.
#   - Implements robust duplicate checking against both the current session and the
#     historical master file based on a 'Title | Company' unique ID.
#   - Efficiently handles search result pagination to reach a user-defined job limit.
#   - Saves unique scraped data incrementally to a session-specific CSV file.
# Author: Stefan Dreyfus
# ==========================================================

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import pandas as pd
from pathlib import Path
import re
import sys
from .jobs_ch_base import get_driver, accept_cookies_and_close_banner


CSV_DELIMITER = ';'

def scrape_jobs(job_search_term: str, max_jobs_to_scrape: int, save_file_path: Path, master_file_path: Path):

    # Clean the job name for file naming (e.g., 'Data Scientist' -> 'data_scientist')
    safe_job_name = re.sub(r'\s+', '_', job_search_term.strip().lower())
    safe_job_name = re.sub(r'[^a-z0-9_]', '', safe_job_name)

    # --- CONFIGURATION ---
    JOB_LINK_XPATH = "//a[@data-cy='job-link']"
    JOB_TITLE_XPATH = ".//div/span[contains(@class, 'textStyle_h6')]"
    COMPANY_NAME_XPATH = "./div/div[4]/p/strong"
    JOB_LOCATION_XPATH = "./div/div[3]/div[1]/p"
    NEXT_PAGE_XPATH = "//a[@data-cy='paginator-next']"

    # CRITICAL XPATH for dual scraping
    SHARED_LIST_CLASS = "li-t_disc"
    TASKS_XPATH = f"//ul[contains(@class, '{SHARED_LIST_CLASS}')][1]//li" #assuming tasks being at the first place in a job ad
    SKILLS_XPATH = f"//ul[contains(@class, '{SHARED_LIST_CLASS}')][2]//li" #assuming skills being at the second place in a job ad
    # ---------------------


    # --- HELPER FUNCTION FOR DUPLICATE CHECKING ---

    def load_unique_ids(file_path):
        """Loads unique IDs (Title | Company) from an existing CSV."""
        unique_ids = set()
        try:
            if file_path.exists() and file_path.stat().st_size > 0:
                df_existing = pd.read_csv(file_path, sep = CSV_DELIMITER)
                if not df_existing.empty and 'Company_Name' in df_existing.columns:
                    df_existing['Unique_ID'] = df_existing['Job_Title'].astype(str).str.strip() + ' | ' + df_existing[
                        'Company_Name'].astype(str).str.strip()
                    unique_ids = set(df_existing['Unique_ID'])
        except Exception as e:
            print(f"WARNING: Error reading CSV at {file_path}. Error: {e}")
        return unique_ids


    # --- INITIAL DATA LOADING ---
    jobs_scraped_count = 0
    scraped_data = []  # Data collected in the current session
    unique_job_ids_session = set()  # Unique IDs collected in the current session

    # Load existing IDs from the session-specific file
    unique_job_ids_session = load_unique_ids(save_file_path)
    jobs_scraped_count = len(unique_job_ids_session)

    # Load ALL unique IDs from the master file
    unique_job_ids_master = load_unique_ids(master_file_path)

    print("-" * 50)
    if jobs_scraped_count > 0:
        print(f"RESUMING SCRAPE for '{job_search_term}': Loaded {jobs_scraped_count} existing records from session file.")
    else:
        print(f"Starting fresh scrape for: '{job_search_term}'.")
    print(f"Targeting {max_jobs_to_scrape} total jobs.")
    print(f"Total unique IDs loaded from MASTER file for cross-check: {len(unique_job_ids_master)}")
    print("-" * 50)

    current_page = 1

    # Getting the URL and accepting cookies and close banner
    driver = get_driver()
    driver.get("https://www.jobs.ch/de/")
    accept_cookies_and_close_banner(driver)

    # Search for the user-specified job title
    wait = WebDriverWait(driver, 5)
    try:
        search_bar = wait.until(
            EC.presence_of_element_located((By.XPATH, "//*[@id='synonym-typeahead-text-field']")))
        search_bar.clear()
        search_bar.send_keys(job_search_term)
        search_bar.send_keys(Keys.RETURN)
        time.sleep(5)
    except Exception as e:
        print(f"Error during initial search: {e}")
        driver.quit()
        exit()


    # --- HELPER FUNCTION FOR SKILL/TASK EXTRACTION ---
    def extract_list(driver, wait, xpath, field_name, job_details):
        """Handles extraction of a specific list (Tasks or Skills) using its XPath."""
        extracted_items = []
        job_details[field_name] = f"no {field_name.lower()} found on this job ad"

        try:
            elements = wait.until(
                EC.presence_of_all_elements_located((By.XPATH, xpath))
            )

            for element in elements:
                item_text = element.text.strip()
                if item_text:
                    extracted_items.append(item_text)

            if extracted_items:
                job_details[field_name] = " | ".join(extracted_items)
                print(f"    -> Extracted {len(extracted_items)} {field_name}.")
            else:
                print(f"    -> No {field_name} list found.")

        except TimeoutException:
            print(f"    -> Warning: {field_name} list timed out (5s).")
        except Exception as e:
            print(f"    -> Error during {field_name} extraction: {e}")


    # --- JOB ITERATION AND SCRAPING MASTER LOOP (PAGINATION) ---
    while jobs_scraped_count < max_jobs_to_scrape:  # Uses the user-defined max_jobs_to_scrape

        # SCROLL DOWN TO LOAD ALL JOBS ON THE CURRENT PAGE
        try:
            print("Scrolling page content to load all job links on this view...")
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(3)
        except Exception as e:
            print(f"Error during scrolling: {e}")

        # LOCATE ALL JOB LINKS
        try:
            wait.until(EC.presence_of_element_located((By.XPATH, JOB_LINK_XPATH)))
            job_links_on_page = driver.find_elements(By.XPATH, JOB_LINK_XPATH)
        except TimeoutException:
            print(f"No job ads found on page {current_page}. Stopping.")
            break

        num_jobs_on_page = len(job_links_on_page)
        num_to_scrape_on_page = min(num_jobs_on_page, max_jobs_to_scrape - jobs_scraped_count)

        print(f"Found {num_jobs_on_page} links. Checking the next {num_to_scrape_on_page} job(s)...")

        # ITERATE AND SCRAPE JOBS
        for i in range(num_jobs_on_page):

            if jobs_scraped_count >= max_jobs_to_scrape:
                break

            job_details = {"Job_Index": jobs_scraped_count + 1,
                           "Job_Title": "N/A",
                           "Company_Name": "N/A",
                           "Job_Location": "N/A",
                           "Tasks": "no tasks found on this job ad",
                           "Skills": "no skills found on this job ad",
                           "Job_Search_Term": job_search_term}
            unique_id = None

            # NAVIGATION AND INITIAL EXTRACTION (FROM SEARCH RESULTS)
            try:
                job_links = wait.until(EC.presence_of_all_elements_located((By.XPATH, JOB_LINK_XPATH)))
                current_link = job_links[i]

                # Extract Title, Company, and Location
                job_title = current_link.find_element(By.XPATH, JOB_TITLE_XPATH).text.strip()
                company_name = current_link.find_element(By.XPATH, COMPANY_NAME_XPATH).text.strip()

                try:
                    location_element = current_link.find_element(By.XPATH, JOB_LOCATION_XPATH)
                    job_location = location_element.text.strip()
                    job_details["Job_Location"] = job_location
                except NoSuchElementException:
                    job_details["Job_Location"] = "Location N/A (Search View)"

                unique_id = f"{job_title} | {company_name}"

            except Exception as e:
                print(f"Could not extract basic info for job link at index {i}. Skipping. Error: {e}")
                continue

            # DUPLICATE CHECKS
            if unique_id in unique_job_ids_session:
                print(f"  -> Duplicate found in SESSION FILE: '{job_title[:50]}...' (Skipping)")
                continue

            if unique_id in unique_job_ids_master:
                print(f"  -> Duplicate found in MASTER FILE: '{job_title[:50]}...' (Skipping)")
                continue

            # Job is unique. Set details and proceed to click.
            job_details["Job_Title"] = job_title
            job_details["Company_Name"] = company_name


            print(
                f"\n--- Scraping UNIQUE Job {jobs_scraped_count + 1}/{max_jobs_to_scrape}: {job_title[:100]} ({company_name[:50]})... ---")

            try:
                # Click the job link to open details
                driver.execute_script("arguments[0].click();", current_link)
                time.sleep(3)  # Wait for the detail pane content to update

            except Exception as e:
                print(f"Could not navigate to unique job ad. Skipping. Error: {e}")
                continue

            # DUAL EXTRACTION LOGIC (TASKS and SKILLS)
            extract_list(driver, wait, TASKS_XPATH, "Tasks", job_details)
            extract_list(driver, wait, SKILLS_XPATH, "Skills", job_details)

            # SAVE UNIQUE JOB
            scraped_data.append(job_details)
            unique_job_ids_session.add(unique_id)
            unique_job_ids_master.add(unique_id)
            jobs_scraped_count += 1

            try:
                df_new_job = pd.DataFrame([job_details])

                # Save to Session-Specific CSV
                session_file_exists = save_file_path.exists() and save_file_path.stat().st_size > 0
                df_new_job.to_csv(save_file_path,
                                  mode='a',
                                  header=not session_file_exists,
                                  index=False,
                                  sep = CSV_DELIMITER)

                print(f"    -> UNIQUE Data Appended to Session CSVs. Total records: {jobs_scraped_count}")
            except Exception as e:
                print(f"WARNING: Could not save intermediate data to CSV. Error: {e}")

        # PAGINATE
        if jobs_scraped_count >= max_jobs_to_scrape:
            print(f"Limit of {max_jobs_to_scrape} jobs reached.")
            break

        # Attempt to click the next page button
        try:
            next_page_link = wait.until(
                EC.element_to_be_clickable((By.XPATH, NEXT_PAGE_XPATH))
            )
            driver.execute_script("arguments[0].click();", next_page_link)
            print(f"Successfully moved to page {current_page + 1}.")
            time.sleep(5)
            current_page += 1

        except TimeoutException:
            print("No 'Next Page' found. All available results scraped.")
            break
        except Exception as e:
            print(f"Error clicking the next page: {e}. Stopping pagination.")
            break

    # --- FINAL OUTPUT ---
    pd.set_option('display.width', 1000)
    df_skills = pd.DataFrame(scraped_data)

    print("\n" + "=" * 50)
    print(f"Successfully scraped {len(df_skills)} NEW job ads for '{job_search_term}'.")
    print("=" * 50)
    if not df_skills.empty:
        print(df_skills[['Job_Index', 'Job_Title', 'Company_Name', 'Job_Location', 'Tasks', 'Skills']].to_string())
    else:
        print("No new unique jobs were scraped in this session.")
    print("=" * 50)

    if driver: driver.quit()

    return df_skills
# --- STANDALONE EXECUTION BLOCK ---
if __name__ == "__main__":

    print("--- RUNNING SCRAPER IN STANDALONE TEST MODE ---")

    # --- USER INPUT AND DYNAMIC CONFIGURATION ---
    job_search_term = input("Enter the job title you want to scrape (e.g., Data Scientist): ")
    while True:
        try:
            max_jobs_input = input("Enter the maximum number of jobs to scrape (e.g., 50): ")
            MAX_JOBS_TO_SCRAPE_TEST = int(max_jobs_input)
            if MAX_JOBS_TO_SCRAPE_TEST <= 0:
                print("Please enter a positive number.")
                continue
            break
        except ValueError:
            print("Invalid input. Please enter a whole number.")

    # Define paths relative to THIS script for robust standalone testing
    PROJECT_ROOT_TEST = Path(__file__).resolve().parent.parent.parent
    RAW_DATA_DIR_TEST = PROJECT_ROOT_TEST / "data" / "raw"

    # Ensure raw directory exists for saving
    RAW_DATA_DIR_TEST.mkdir(parents=True, exist_ok=True)

    safe_job_name = re.sub(r'\s+', '_', job_search_term.strip().lower())
    safe_job_name = re.sub(r'[^a-z0-9_]', '', safe_job_name)

    # Use TEST paths
    TEST_SAVE_FILE_PATH = RAW_DATA_DIR_TEST / f"jobs_ch_{safe_job_name}_skills.csv"
    TEST_MASTER_FILE_PATH = RAW_DATA_DIR_TEST / "jobs_ch_skills_all.csv"

    # Call the main function with the user inputs
    scrape_jobs(job_search_term, MAX_JOBS_TO_SCRAPE_TEST, TEST_SAVE_FILE_PATH, TEST_MASTER_FILE_PATH)