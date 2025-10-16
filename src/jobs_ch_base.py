# --- IMPORTS ---
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import platform

# --- SYSTEM OS DETECTION ---
system = platform.system()

# Set a simplified OS type for logic checks (Mac, Windows, Linux/Fallback)
if system == "Darwin":
    # Darwin is the core OS name for macOS/OS X
    detected_os = "Mac"
elif system == "Windows":
    detected_os = "Windows"
elif system == "Linux":
    detected_os = "Linux"
else:
    # Catch any other Unix-like or unknown system
    print(f"WARNING: Unknown OS '{system}'. Falling back to general Windows configuration.")
    detected_os = "Windows"

# --- DRIVER CONFIGURATION (get_driver) ---
# Driver Configuration and OS Detection
def get_driver(os_type="Windows"):  # os_type parameter can be used for User-Agent selection
    """Start Chrome with options using webdriver-manager for automatic driver management."""
    options = Options()
    options.add_argument("--start-maximized")

    if os_type == "Mac":
        user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) ..."
    elif os_type == "Linux":
        # Necessary Linux flags
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        user_agent = "Mozilla/5.0 (X11; Linux x86_64) ..."
    else:  # Windows and Fallback
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) ..."

    options.add_argument(f"--user-agent={user_agent}")

    # CRITICAL: Use the Service object with webdriver-manager
    service = ChromeService(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=options)


# --- Cookie and Banner Management ---
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


# Simple test run to check that banners are handled
if __name__ == "__main__":
    driver = get_driver(detected_os)
    driver.get("https://www.jobs.ch/de/")
    accept_cookies_and_close_banner(driver)
    time.sleep(5)
    driver.quit()