from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException
from jobs_ch_base import get_driver, accept_cookies_and_close_banner
import time
import pandas as pd
from pathlib import Path

# --- CONFIGURATION ---
MAX_JOBS_TO_SCRAPE = 30  # Set desired job ads scraping limit here
JOB_LINK_XPATH = "//a[@data-cy='job-link']"
JOB_TITLE_XPATH = ".//div/span[contains(@class, 'textStyle_h6')]"
COMPANY_NAME_XPATH = "./div/div[4]/p/strong"
REQUIRED_SKILLS_CLASSES = "li-t_disc pl_s16 mb_s40 mt_s16"

# Skill Text Normalization and Cleaning
NEXT_PAGE_XPATH = "//a[@data-cy='paginator-next']"

# CRITICAL XPATH FIX
class_conditions = "') and contains(@class, '".join(REQUIRED_SKILLS_CLASSES.split(' '))
REQUIRED_SKILLS_XPATH = f"//ul[contains(@class, '{class_conditions}')]"
# ---------------------

# Dynamic Path Configuration for Cross-Platform/GitHub Compatibility
# Get the path to the currently running script
BASE_DIR = Path(__file__).resolve().parent

# Going up one level (to the project root) and then down to 'data/raw'. This creates the target directory path: Pycharm_CIP_Jobs_Project_Github/data/raw
DATA_DIR = BASE_DIR.parent / "data" / "raw"

#Ensuring the target directory exists. If not, it will be created
DATA_DIR.mkdir(parents=True, exist_ok=True)

# Constructing the final absolute path for the CSV file
SAVE_FILE_PATH = DATA_DIR / "jobs_ch_data_science_skills.csv"

# --- Checking if resuming script after an error etc ---
jobs_scraped_count = 0
scraped_data = []
unique_job_ids = set()  # Set for fast checking of duplicates

try:
    if SAVE_FILE_PATH.exists() and SAVE_FILE_PATH.stat().st_size > 0:
        df_existing = pd.read_csv(SAVE_FILE_PATH)

        if not df_existing.empty and 'Company_Name' in df_existing.columns:
            # Load existing records into the in-memory list
            scraped_data = df_existing.to_dict('records')
            jobs_scraped_count = len(scraped_data)

            # Create a set of unique IDs (Title | Company) for O(1) duplicate checks
            df_existing['Unique_ID'] = df_existing['Job_Title'].astype(str).str.strip() + ' | ' + df_existing[
                'Company_Name'].astype(str).str.strip()
            unique_job_ids = set(df_existing['Unique_ID'])

            print("-" * 50)
            print(f"RESUMING SCRAPE: Loaded {jobs_scraped_count} existing records from CSV.")
            print(f"Total unique IDs loaded for duplication check: {len(unique_job_ids)}")
            print("-" * 50)
        else:
            print("Existing save file is empty or missing necessary columns. Starting from scratch.")
    else:
        print("Starting fresh: CSV file not found or is empty.")

except Exception as e:
    print(f"WARNING: Error reading existing CSV. Starting from scratch. Error: {e}")
    # Variables are already initialized for a fresh start

current_page = 1

# Getting the URL and accepting cookies and close banner
driver = get_driver()
driver.get("https://www.jobs.ch/de/")
accept_cookies_and_close_banner(driver)

# Search for Data Science in Search bar
wait = WebDriverWait(driver, 5)
try:
    search_bar = wait.until(
        EC.presence_of_element_located((By.XPATH, "//*[@id='synonym-typeahead-text-field']")))
    search_bar.clear()
    search_bar.send_keys("Data Science")
    search_bar.send_keys(Keys.RETURN)
    time.sleep(5)
except Exception as e:
    print(f"Error during initial search: {e}")
    driver.quit()
    exit()


# Master loop that continues until the limit is reached or there's no next page
while jobs_scraped_count < MAX_JOBS_TO_SCRAPE:

    # 1. SCROLL DOWN TO LOAD ALL JOBS ON THE CURRENT PAGE AGAINST LAZY LOADING

    try:
        print("Scrolling page content to load all job links on this view...")
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)
    except Exception as e:
        print(f"Error during scrolling: {e}")

    # 2. LOCATE ALL JOB LINKS FOR ITERATION on the currently loaded page
    try:
        # Wait for the first job link to ensure the page has loaded
        wait.until(EC.presence_of_element_located((By.XPATH, JOB_LINK_XPATH)))
        job_links_on_page = driver.find_elements(By.XPATH, JOB_LINK_XPATH)
    except TimeoutException:
        print(f"No job ads found on page {current_page}. Stopping.")
        break

    num_jobs_on_page = len(job_links_on_page)
    num_to_scrape_on_page = min(num_jobs_on_page, MAX_JOBS_TO_SCRAPE - jobs_scraped_count)

    print(f"Found {num_jobs_on_page} links. Scraping the next {num_to_scrape_on_page} job(s)...")


    # 3. ITERATE AND SCRAPE JOBS
    # Starting  from the first job (index 0) and check for duplicates
    for i in range(num_jobs_on_page):

        if jobs_scraped_count >= MAX_JOBS_TO_SCRAPE:
            break

        job_details = {"Job_Index": jobs_scraped_count + 1,
                       "Job_Title": "N/A",
                       "Company_Name": "N/A",
                       "Skills": "no skills found on this job ad"}
        required_skills = []
        unique_id = None  # Initialize unique_id

        # --- NAVIGATION AND INITIAL EXTRACTION ---
        try:
            job_links = wait.until(EC.presence_of_all_elements_located((By.XPATH, JOB_LINK_XPATH)))
            current_link = job_links[i]

            # Extract Title and Company Name (required for unique ID)
            job_title = current_link.find_element(By.XPATH, JOB_TITLE_XPATH).text.strip()
            company_name = current_link.find_element(By.XPATH, COMPANY_NAME_XPATH).text.strip()

            unique_id = f"{job_title} | {company_name}"

        except Exception as e:
            # Failed to get basic info (Title/Company). Skip this link.
            print(f"Could not extract basic info for job link at index {i}. Skipping. Error: {e}")
            continue

        # --- DUPLICATE CHECK ---
        if unique_id in unique_job_ids:
            print(f"  -> Duplicate found: '{job_title[:50]} | {company_name[:30]}' (Skipping)")
            continue

        # Job is unique. Set details and proceed to click.
        job_details["Job_Title"] = job_title
        job_details["Company_Name"] = company_name

        print(
            f"\n--- Scraping UNIQUE Job {jobs_scraped_count + 1}/{MAX_JOBS_TO_SCRAPE}: {job_title[:100]} ({company_name[:50]})... ---")

        try:
            # Click the job link
            driver.execute_script("arguments[0].click();", current_link)
            time.sleep(3)  # Wait for the detail pane content to update

        except Exception as e:
            print(f"Could not navigate to unique job ad. Skipping. Error: {e}")
            # If navigation fails, we DON'T increment the count or save, just continue
            continue


        # --- SAVE UNIQUE JOB ---
        scraped_data.append(job_details)
        unique_job_ids.add(unique_id)  # Add new ID to the set
        jobs_scraped_count += 1

        try:
            # CRITICAL CHANGE: Save the single new job in APPEND MODE ('a')
            # Only include headers if the file is new (jobs_scraped_count == 1)
            df_new_job = pd.DataFrame([job_details])
            df_new_job.to_csv(SAVE_FILE_PATH, mode='a', header=(jobs_scraped_count == 1), index=False)

            print(f"    -> UNIQUE Data Appended to CSV. Total records: {jobs_scraped_count}")
        except Exception as e:
            print(f"WARNING: Could not save intermediate data to CSV. Error: {e}")

    # 4. PAGINATE: Check for the Next Page button after scraping the current set
    if jobs_scraped_count >= MAX_JOBS_TO_SCRAPE:
        print(f"Limit of {MAX_JOBS_TO_SCRAPE} jobs reached.")
        break

    # Attempt to click the next page button
    try:
        next_page_link = wait.until(
            EC.element_to_be_clickable((By.XPATH, NEXT_PAGE_XPATH))
        )
        # JavaScript click for robustness
        driver.execute_script("arguments[0].click();", next_page_link)
        print(f"Successfully moved to page {current_page + 1}.")
        time.sleep(5)  # Give ample time for the new results page to load
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

# Print comprehensive skill list
all_individual_skills = []
for skills_string in df_skills['Skills']:
    if skills_string and skills_string != "no skills found on this job ad":
        individual_skills = [s.strip() for s in skills_string.split(' | ')]
        all_individual_skills.extend(individual_skills)
unique_skills_list = sorted(list(set(all_individual_skills)))

print("\n" + "#" * 50)
print("LIST OF ALL UNIQUE SCRAPED REQUIRED SKILLS")
print("#" * 50)
for i, skill in enumerate(unique_skills_list):
    print(f"  {i + 1}. {skill}")
print("#" * 50)

print("\n" + "=" * 50)
print(f"Successfully scraped {len(df_skills)} job ads:")
print("=" * 50)
print(df_skills[['Job_Index', 'Job_Title', 'Skills']].to_string())
print("=" * 50)


driver.quit()