import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from jobs_ch_base import get_driver, accept_cookies_and_close_banner

#Getting the URL and accepting cookies and close banner
driver = get_driver()
driver.get("https://www.jobs.ch/de/")
accept_cookies_and_close_banner(driver)

#Search for Data Science in Search bar
wait = WebDriverWait(driver, 5)
search_bar = wait.until(
    EC.presence_of_element_located((By.XPATH, "//*[@id='synonym-typeahead-text-field']"))
)
search_bar.clear()
search_bar.send_keys("Data Science")
search_bar.send_keys(Keys.RETURN)

#Fetching the required skills
wait = WebDriverWait(driver, 15)
job_cards = wait.until(
    EC.presence_of_all_elements_located((By.XPATH, "//div[@data-cy='vacancy-serp-item']"))
)

all_jobs = []
for job in job_cards:
    if len(all_jobs) >= 5:
        break  # Only first 5 jobs with skills

    try:
        driver.execute_script("arguments[0].scrollIntoView();", job)
        job.click()

        # wait for job panel to appear and stabilize
        time.sleep(1.5)  # short delay for dynamic content

        # grab all <ul> inside the job panel
        job_detail = driver.find_element(By.ID, "job-ad-details-section")
        skills_elements = job_detail.find_elements(By.XPATH, ".//ul[contains(@class,'li-t_disc')]//li//span | .//ul[contains(@class,'li-t_disc')]//li")

        skills = [el.text.strip() for el in skills_elements if el.text.strip()]

        if not skills:
            print("No skills section found for this job, skipping...")
            continue

        title = job.find_element(By.XPATH, ".//span[contains(@class,'textStyle_h6')]").text
        all_jobs.append({"title": title, "skills": skills})

    except Exception as e:
        print(f"Error extracting job: {e}")
        continue

for job in all_jobs:
    print("Job Title:", job['title'])
    print("Skills:")
    for skill in job['skills']:
        print("-", skill)
    print("\n" + "-"*40 + "\n")

input("Press ENTER to close the browser...")
driver.quit()
