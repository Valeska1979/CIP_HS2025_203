from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from jobs_ch_base import get_driver, accept_cookies_and_close_banner
import time

# --- Setup driver and open page ---
driver = get_driver()
driver.get("https://www.jobs.ch/de/")
accept_cookies_and_close_banner(driver)

# --- Search for Data Science ---
wait = WebDriverWait(driver, 5)
search_bar = wait.until(
    EC.presence_of_element_located((By.XPATH, "//*[@id='synonym-typeahead-text-field']"))
)
search_bar.clear()
search_bar.send_keys("Data Science")
search_bar.send_keys(Keys.RETURN)

# Wait for search results to load
wait = WebDriverWait(driver, 15)
job_cards = wait.until(
    EC.presence_of_all_elements_located((By.XPATH, "//div[@data-cy='vacancy-serp-item']"))
)

all_jobs = []

# --- Loop through first 5 jobs only ---
for job in job_cards[:5]:
    try:
        driver.execute_script("arguments[0].scrollIntoView();", job)
        job.click()

        # Wait a little for the job details panel to load
        time.sleep(1)

        # --- Scrape skills ---
        skills_list = WebDriverWait(driver, 8).until(
            EC.presence_of_all_elements_located(
                (By.XPATH, "//*[@id='job-ad-details-section']//ul[contains(@class, 'li-t_disc')]/li")
            )
        )
        skills = [li.text for li in skills_list]

        # Job title
        title = job.find_element(By.XPATH, ".//span[contains(@class,'textStyle_h6')]").text

        all_jobs.append({"title": title, "skills": skills})
    except Exception as e:
        print(f"Error extracting job: {e}")
        continue

# Print results
for job in all_jobs:
    print(job)

input("Press ENTER to close the browser...")
driver.quit()
