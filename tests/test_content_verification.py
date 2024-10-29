# test_content_verification.py
import pytest
from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.helpers import load_websites_from_yaml


@pytest.mark.parametrize("url", load_websites_from_yaml())
def test_content_verification(url):
    """Verify if a search bar element exists on the page."""
    # Setup Selenium WebDriver
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    driver.get(url)

    # Set an implicit wait for page elements
    driver.implicitly_wait(10)

    try:
        # Increase wait time to handle dynamic loading
        timeout_duration = 20
        search_bar = None

        # Specific patterns for known websites
        if "amazon" in url:
            search_bar = WebDriverWait(driver, timeout_duration).until(
                EC.visibility_of_element_located((By.ID, 'twotabsearchtextbox'))
            )
        elif "bestbuy" in url:
            try:
                search_bar = WebDriverWait(driver, timeout_duration).until(
                    EC.visibility_of_element_located((By.CSS_SELECTOR, "input[aria-label*='Search']"))
                )
            except TimeoutException:
                # Broader fallback pattern
                search_bar = WebDriverWait(driver, timeout_duration).until(
                    EC.visibility_of_element_located(
                        (By.CSS_SELECTOR, "input[name='search'], input[placeholder*='Search']"))
                )
        elif "kohls" in url:
            search_bar = WebDriverWait(driver, timeout_duration).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, "input[placeholder='Search']"))
            )
        else:
            # Generic pattern for other websites
            search_bar = WebDriverWait(driver, timeout_duration).until(
                EC.visibility_of_any_elements_located(
                    [(By.CSS_SELECTOR, "input[type='search']"),
                     (By.NAME, 'q'),
                     (By.CSS_SELECTOR, "input[class*='search']")]
                )
            )

        # Assert that the search bar is found and visible
        assert search_bar is not None, f"{url} has no identifiable search bar"

    except Exception as e:
        pytest.fail(f"Content verification failed for {url} due to error: {e}")

    finally:
        # Close the browser after test completion
        driver.quit()