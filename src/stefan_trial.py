from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from jobs_ch_base import get_driver, accept_cookies_and_close_banner

#Getting the URL and accepting cookies and close banner
driver = get_driver()
driver.get("https://www.jobs.ch/de/")

accept_cookies_and_close_banner(driver)

#Looking for Data Science in Search bar
wait = WebDriverWait(driver, 3)
search_bar = wait.until(
    EC.presence_of_element_located(
        (By.XPATH, "//*[@id='synonym-typeahead-text-field']")))

search_bar.clear() #clear search par if needed
search_bar.send_keys("Data Science")
search_bar.send_keys(Keys.RETURN) #pressing Enter / Search for the job

