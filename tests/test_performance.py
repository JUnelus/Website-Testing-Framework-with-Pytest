# test_performance.py
import pytest
import time
from helpers import load_websites_from_yaml, fetch_url

@pytest.mark.parametrize("url", load_websites_from_yaml())
def test_performance(url):
    """Test if website loads within a reasonable time (e.g., 3 seconds)."""
    start_time = time.time()
    try:
        response = fetch_url(url)
        load_time = time.time() - start_time
        assert load_time < 3, f"{url} took too long to load: {load_time:.2f} seconds"
    except Exception as e:
        pytest.fail(f"Performance test failed for {url} due to error: {e}")
