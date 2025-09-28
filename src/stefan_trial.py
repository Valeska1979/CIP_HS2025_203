from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from jobs_ch_base import get_driver, accept_cookies_and_close_banner
import time
import pandas as pd

#Getting the URL and accepting cookies and close banner
driver = get_driver()
driver.get("https://www.jobs.ch/de/")

accept_cookies_and_close_banner(driver)

#Search for Data Science in Search bar
wait = WebDriverWait(driver, 3)
search_bar = wait.until(
    EC.presence_of_element_located(
        (By.XPATH, "//*[@id='synonym-typeahead-text-field']")))

search_bar.clear() #clear search par if needed
search_bar.send_keys("Data Science")
search_bar.send_keys(Keys.RETURN) #pressing Enter / Search for the job

time.sleep(5)

all_jobs = []








#Fetching the required skills

wait = WebDriverWait(driver, 5)
skills_list = wait.until(
    EC.presence_of_all_elements_located(
        (By.XPATH, "//*[@id='job-ad-details-section']//ul[contains(@class, 'li-t_disc')]/li")))

# Extract text from each <li>
skills = [li.text for li in skills_list]
print(skills)



input("Press ENTER to close the browser...") # for testing purpose, window stays open until ENTER is pressed
