from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time

def get_driver():
    """Start Chrome with options (User-Agent to avoid 403 errors)."""
    options = Options()
    options.add_argument("--start-maximized")
    options.add_argument("--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                         "AppleWebKit/537.36 (KHTML, like Gecko) "
                         "Chrome/140.0.0.0 Safari/537.36")
    return webdriver.Chrome(options=options)

def accept_cookies_and_close_banner(driver):
    """Accept cookies and close the smart search popup if present."""
    wait = WebDriverWait(driver, 10)

    # 1. Cookie banner
    try:
        cookie_btn = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(text(), 'Alle Cookies akzeptieren')]")
            )
        )
        cookie_btn.click()
        print("Cookie banner accepted")
    except TimeoutException:
        print("No cookie banner found")

    # 2. Smart search banner
    try:
        close_btn = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(text(), 'Schliessen')]")
            )
        )
        close_btn.click()
        print("Smart search banner closed")
    except TimeoutException:
        print("No smart search banner found")

if __name__ == "__main__":
    # Simple test run to check that banners are handled
    driver = get_driver()
    driver.get("https://www.jobs.ch/de/")

    accept_cookies_and_close_banner(driver)

    time.sleep(5)  # Just to visually confirm before quitting
    driver.quit()
