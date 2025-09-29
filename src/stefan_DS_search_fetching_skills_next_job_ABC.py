from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException, \
    ElementClickInterceptedException
# Assuming jobs_ch_base contains get_driver and accept_cookies_and_close_banner
from jobs_ch_base import get_driver, accept_cookies_and_close_banner
import time
import pandas as pd

# --- CONFIGURATION ---
MAX_JOBS_TO_SCRAPE = 5
JOB_LINK_XPATH = "//a[@data-cy='job-link']"
JOB_TITLE_XPATH = ".//div/span[contains(@class, 'textStyle_h6')]"
REQUIRED_SKILLS_CLASSES = "li-t_disc pl_s16 mb_s40 mt_s16"

# **CRITICAL XPATH FIX: Correctly build the robust XPath for the <ul> skills list**
class_conditions = "') and contains(@class, '".join(REQUIRED_SKILLS_CLASSES.split(' '))
REQUIRED_SKILLS_XPATH = f"//ul[contains(@class, '{class_conditions}')]"
# ---------------------

# Getting the URL and accepting cookies and close banner
driver = get_driver()
driver.get("https://www.jobs.ch/de/")
accept_cookies_and_close_banner(driver)

# Search for Data Science in Search bar
wait = WebDriverWait(driver, 10)  # Using 10s wait for robustness
try:
    search_bar = wait.until(
        EC.presence_of_element_located(
            (By.XPATH, "//*[@id='synonym-typeahead-text-field']")))

    search_bar.clear()  # clear search par if needed
    search_bar.send_keys("Data Science")
    search_bar.send_keys(Keys.RETURN)  # pressing Enter / Search for the job

    time.sleep(5)  # Wait for the search results page to load completely

except Exception as e:
    print(f"Error during initial search: {e}")
    driver.quit()
    exit()

# --- JOB ITERATION AND SCRAPING LOOP ---
scraped_data = []

try:
    # Get the initial list of all job links (cards)
    job_links = wait.until(
        EC.presence_of_all_elements_located((By.XPATH, JOB_LINK_XPATH))
    )
except TimeoutException:
    print("No job ads found on the results page.")
    driver.quit()
    exit()

num_jobs_to_scrape = min(len(job_links), MAX_JOBS_TO_SCRAPE)
print(f"Found {len(job_links)} jobs. Scraping the first {num_jobs_to_scrape}...")

for i in range(num_jobs_to_scrape):
    job_details = {"Job_Index": i + 1, "Job_Title": "N/A", "Skills": "no skills found on this job ad"}
    required_skills = []

    # 1. Re-locate the elements in EVERY iteration to prevent StaleElementReferenceException
    try:
        job_links = wait.until(
            EC.presence_of_all_elements_located((By.XPATH, JOB_LINK_XPATH))
        )
        current_link = job_links[i]

        # Extract Job Title for logging
        try:
            job_title_element = current_link.find_element(By.XPATH, JOB_TITLE_XPATH)
            job_title = job_title_element.text.strip()
            job_details["Job_Title"] = job_title
        except NoSuchElementException:
            job_title = f"Job {i + 1} (Title not found)"
            job_details["Job_Title"] = job_title

        print(f"\n--- Scraping Job {i + 1}/{num_jobs_to_scrape}: {job_title[:50]}... ---")

        # 2. Click the job link to load the details in the right pane

        # **FIX 1: Use JavaScript click to bypass ElementClickInterceptedException**
        # **FIX 2: Increased wait time after click to ensure detail panel loads**
        try:
            driver.execute_script("arguments[0].click();", current_link)
            time.sleep(3)  # Increased sleep to 3 seconds for detail pane content load
        except Exception as click_error:
            # If JS click fails (rare), fall back to standard click with a higher wait
            print(f"⚠️ JS click failed (Job {i + 1}). Falling back to standard click. Error: {click_error}")
            current_link.click()
            time.sleep(4)  # Even longer wait for stability

    except Exception as e:
        print(f"Could not navigate to job ad {i + 1}. Skipping. Error: {e}")
        continue  # Skip to the next job

    # 3. Skill Extraction
    try:
        # Find ALL <ul> elements with the unique content classes
        all_content_lists = wait.until(
            EC.presence_of_all_elements_located((By.XPATH, REQUIRED_SKILLS_XPATH))
        )

        # Heuristic: Take the last list matching the pattern (most likely the skills section)
        if all_content_lists:
            skills_list_ul = all_content_lists[-1]
        else:
            raise Exception("Found no content lists matching the class pattern.")

        # **FIX 3: Loop through ALL list items (<li>) within the identified skills <ul>**
        skill_items = skills_list_ul.find_elements(By.TAG_NAME, "li")
        for skill_item in skill_items:
            # Recursively get all text from the list item, including nested elements
            skill_text = skill_item.get_attribute('textContent').strip()
            # Clean up excessive whitespace/newlines that textContent might include
            skill_text = ' '.join(skill_text.split())
            if skill_text:
                required_skills.append(skill_text)

        if required_skills:
            job_details["Skills"] = " | ".join(required_skills)  # Used "|" as a clear separator
            print(f"✅ Skills Found: {len(required_skills)} items, starting with: {required_skills[0]}...")
        else:
            print("❌ no skills found on this job ad")

    except Exception as e:
        job_details["Skills"] = "no skills found on this job ad"
        print(f"❌ Error during skill extraction for {job_title}. Error: {e}")

    scraped_data.append(job_details)

# --- FINAL OUTPUT ---

# Ensure max_colwidth is set to None for full content display
# NOTE: This line is often necessary even if you use .to_string() below
pd.set_option('display.max_colwidth', None)

df_skills = pd.DataFrame(scraped_data)

print("\n" + "="*50)
print(f"Successfully scraped {len(df_skills)} job ads:")
print("="*50)

# Use .to_string() without arguments to suppress column alignment
# This will fix the massive horizontal whitespace padding
print(df_skills[['Job_Index', 'Job_Title', 'Skills']].to_string())

print("="*50)

# Assuming the previous code block runs successfully and df_skills is available

# 1. Create a list to hold all individual skills
all_individual_skills = []

# 2. Iterate through the 'Skills' column of the DataFrame
for skills_string in df_skills['Skills']:
    # Only process entries that successfully found skills
    if skills_string and skills_string != "no skills found on this job ad":
        # Split the combined string by the custom delimiter ' | '
        individual_skills = [s.strip() for s in skills_string.split(' | ')]
        all_individual_skills.extend(individual_skills)

# 3. Optional: Remove duplicates and sort the list (recommended for a "master list")
unique_skills_list = sorted(list(set(all_individual_skills)))

# 4. Print the final, comprehensive list
print("\n" + "#" * 50)
print("COMPREHENSIVE LIST OF ALL UNIQUE SCRAPED REQUIRED SKILLS")
print("#" * 50)

# Print each skill on a new line for clarity
for i, skill in enumerate(unique_skills_list):
    print(f"  {i+1}. {skill}")

print("#" * 50)

# NOTE: Keep the original DataFrame printout (with the .to_string() fix)
# if you still want to see the job-by-job summary.
print("\nJob-by-Job Summary:")
pd.set_option('display.max_colwidth', None)
print(df_skills[['Job_Index', 'Job_Title', 'Skills']].to_string())
print("="*50)

driver.quit()