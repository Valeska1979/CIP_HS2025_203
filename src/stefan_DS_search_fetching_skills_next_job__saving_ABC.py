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
MAX_JOBS_TO_SCRAPE = 10  # Set desired job ads scraping limit here
JOB_LINK_XPATH = "//a[@data-cy='job-link']"
JOB_TITLE_XPATH = ".//div/span[contains(@class, 'textStyle_h6')]"
REQUIRED_SKILLS_CLASSES = "li-t_disc pl_s16 mb_s40 mt_s16"

# Skill Text Normalization and Cleaning
NEXT_PAGE_XPATH = "//a[@data-cy='paginator-next']"

# CRITICAL XPATH FIX (No change)
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

# --- JOB ITERATION AND SCRAPING MASTER LOOP (PAGINATION) ---
scraped_data = []
jobs_scraped_count = 0
current_page = 1

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
    for i in range(num_to_scrape_on_page):

        if jobs_scraped_count >= MAX_JOBS_TO_SCRAPE:
            break

        job_details = {"Job_Index": jobs_scraped_count + 1, "Job_Title": "N/A",
                       "Skills": "no skills found on this job ad"}
        required_skills = []

        # RE-LOCATE the job links list in every loop to avoid StaleElementReferenceException
        try:
            # Re-fetch the list every time as the detail panel messes up the DOM
            job_links = wait.until(EC.presence_of_all_elements_located((By.XPATH, JOB_LINK_XPATH)))
            current_link = job_links[i]

            # Extract Job Title
            try:
                job_title = current_link.find_element(By.XPATH, JOB_TITLE_XPATH).text.strip()
                job_details["Job_Title"] = job_title
            except NoSuchElementException:
                job_title = f"Job {jobs_scraped_count + 1} (Title not found)"
                job_details["Job_Title"] = job_title

            print(f"\n--- Scraping Job {jobs_scraped_count + 1}/{MAX_JOBS_TO_SCRAPE}: {job_title[:200]}... ---")

            # Click the job link using JavaScript to bypass overlays and wait
            driver.execute_script("arguments[0].click();", current_link)
            time.sleep(3)  # Wait for the detail pane content to update

        except Exception as e:
            print(f"Could not navigate to job ad {jobs_scraped_count + 1}. Skipping. Error: {e}")
            jobs_scraped_count += 1
            continue

        # Skill Extraction
        try:
            all_content_lists = wait.until(
                EC.presence_of_all_elements_located((By.XPATH, REQUIRED_SKILLS_XPATH))
            )

            if all_content_lists:
                skills_list_ul = all_content_lists[-2] #depends which part is the skills in the job ad: rather in the second or in the third part of the job ad.
                skill_items = skills_list_ul.find_elements(By.TAG_NAME, "li")

                for skill_item in skill_items:
                    skill_text = ' '.join(skill_item.get_attribute('textContent').split())
                    if skill_text:
                        required_skills.append(skill_text)

            if required_skills:
                job_details["Skills"] = " | ".join(required_skills)
                print(f" Skills Found: {len(required_skills)} items, starting with: {required_skills[0]}...")
            else:
                print(" no skills found on this job ad")

        except Exception as e:
            job_details["Skills"] = "no skills found on this job ad"
            print(f" Error during skill extraction for {job_title}. Error: {e}")

        scraped_data.append(job_details)
        jobs_scraped_count += 1


        # Intermediate Save after every job

        try:
            df_current = pd.DataFrame(scraped_data)
            df_current.to_csv(SAVE_FILE_PATH, index=False)
            print(f"    -> Data saved successfully to {SAVE_FILE_PATH.name}. Total records: {len(df_current)}")
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