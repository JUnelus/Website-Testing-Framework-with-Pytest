import pytest
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from helpers import load_websites_from_yaml
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import logging
from time import sleep

# Configure logging
logging.basicConfig(level=logging.INFO)

def get_chrome_driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    driver.set_page_load_timeout(120)  # Set page load timeout
    return driver

def locate_element_with_retry(driver, locator, timeout=60, retries=3, delay=5):
    """Retry locating an element in case of intermittent failures."""
    for i in range(retries):
        try:
            return WebDriverWait(driver, timeout).until(EC.visibility_of_element_located(locator))
        except TimeoutException:
            if i < retries - 1:
                sleep(delay)
                logging.warning(f"Retry {i + 1}/{retries} for locating element: {locator}")
            else:
                raise

@pytest.mark.parametrize("url", load_websites_from_yaml())
def test_content_verification(url):
    driver = get_chrome_driver()
    driver.get(url)
    driver.implicitly_wait(10)

    try:
        timeout_duration = 60
        logging.info(f"Testing URL: {url}")

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))

        # Site-specific locators
        if "amazon" in url:
            try:
                search_bar = locate_element_with_retry(driver, (By.ID, 'twotabsearchtextbox'), timeout_duration)
            except TimeoutException:
                logging.warning(f"Falling back to generic search selector for Amazon on {url}")
                search_bar = locate_element_with_retry(driver, (By.CSS_SELECTOR, "input[type='search']"), timeout_duration)

        elif "bestbuy" in url:
            try:
                search_bar = locate_element_with_retry(driver, (By.CSS_SELECTOR, "input[aria-label*='Search']"), timeout_duration)
            except TimeoutException:
                logging.warning(f"Using broader selector for Best Buy on {url}")
                search_bar = locate_element_with_retry(driver, (By.CSS_SELECTOR, "input[name='search'], input[placeholder*='Search']"), timeout_duration)

        elif "kohls" in url:
            search_bar = locate_element_with_retry(driver, (By.CSS_SELECTOR, "input[placeholder='Search']"), timeout_duration)

        else:
            # General fallback for other sites
            search_bar = locate_element_with_retry(driver, (By.CSS_SELECTOR, "input[type='search'], input[name='q'], input[class*='search']"), timeout_duration)

        assert search_bar is not None, f"{url} has no identifiable search bar"
        logging.info(f"Search bar located on {url}")

    except (TimeoutException, NoSuchElementException) as e:
        pytest.fail(f"Content verification failed for {url} due to error: {e}")

    finally:
        driver.quit()