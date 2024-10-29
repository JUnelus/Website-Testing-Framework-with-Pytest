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

def get_chrome_driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    return webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

@pytest.mark.parametrize("url", load_websites_from_yaml())
def test_content_verification(url):
    """Verify if a search bar element exists on the page."""
    driver = get_chrome_driver()
    driver.get(url)

    # Implicit wait for initial element loading
    driver.implicitly_wait(10)

    try:
        # Adjusted timeout duration
        timeout_duration = 30
        search_bar = None

        # Specific patterns for known websites
        if "amazon" in url:
            try:
                search_bar = WebDriverWait(driver, timeout_duration).until(
                    EC.visibility_of_element_located((By.ID, 'twotabsearchtextbox'))
                )
            except TimeoutException:
                # Broad fallback pattern if Amazon search ID fails
                search_bar = WebDriverWait(driver, timeout_duration).until(
                    EC.visibility_of_element_located((By.CSS_SELECTOR, "input[type='search']"))
                )

        elif "bestbuy" in url:
            try:
                search_bar = WebDriverWait(driver, timeout_duration).until(
                    EC.visibility_of_element_located((By.CSS_SELECTOR, "input[aria-label*='Search']"))
                )
            except TimeoutException:
                # Fallback for Best Buy with broader selector
                search_bar = WebDriverWait(driver, timeout_duration).until(
                    EC.visibility_of_element_located((By.CSS_SELECTOR, "input[name='search'], input[placeholder*='Search']"))
                )

        elif "kohls" in url:
            search_bar = WebDriverWait(driver, timeout_duration).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, "input[placeholder='Search']"))
            )

        else:
            # Generic pattern for other websites
            search_bar = WebDriverWait(driver, timeout_duration).until(
                EC.visibility_of_any_elements_located([
                    (By.CSS_SELECTOR, "input[type='search']"),
                    (By.NAME, 'q'),
                    (By.CSS_SELECTOR, "input[class*='search']")
                ])
            )

        # Assert that the search bar is visible and available
        assert search_bar is not None, f"{url} has no identifiable search bar"

    except (TimeoutException, NoSuchElementException) as e:
        # Fail test with error detail if search element is not found
        pytest.fail(f"Content verification failed for {url} due to error: {e}")

    finally:
        # Ensure browser closes after test
        driver.quit()
