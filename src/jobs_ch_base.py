from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time

user_os = input("Which OS do you use (Windows / Mac / Linux):  ")

if user_os == "Mac":
    def get_driver():
        """Start Chrome with options (User-Agent to avoid 403 errors)."""
        options = Options()
        options.add_argument("--start-maximized")
        options.add_argument("--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                                 "AppleWebKit/537.36 (KHTML, like Gecko) "
                                 "Chrome/140.0.0.0 Safari/537.36")
        return webdriver.Chrome(options=options)
elif user_os == "Windows":

    def get_driver():
        """Start Chrome with options (User-Agent to avoid 403 errors)."""
        options = Options()
        options.add_argument("--start-maximized")
        options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                                 "AppleWebKit/537.36 (KHTML, like Gecko) "
                                 "Chrome/140.0.0.0 Safari/537.36")
        return webdriver.Chrome(options=options)

elif user_os == "Linux":

    def get_driver():
        """Start Chrome with options (User-Agent to avoid 403 errors)."""
        options = Options()
        options.add_argument("--start-maximized")
        options.add_argument("--no-sandbox") #options often required for headless/server Linux environments
        options.add_argument("--disable-dev-shm-usage") #options often required for headless/server Linux environments

        options.add_argument("--user-agent=Mozilla/5.0 (X11; Linux x86_64) "
                             "AppleWebKit/537.36 (KHTML, like Gecko) "
                             "Chrome/140.0.0.0 Safari/537.36")
        return webdriver.Chrome(options=options)

else:
    # CATCH-ALL for typos or unknown OS
    print(f"WARNING: Unknown OS '{user_os}'. Falling back to default Windows configuration.")
    def get_driver():
        """Fallback driver setup."""
        options = Options()
        options.add_argument("--start-maximized")
        options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
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
