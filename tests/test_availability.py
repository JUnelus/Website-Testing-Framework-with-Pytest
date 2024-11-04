import pytest
from helpers import load_websites_from_yaml, fetch_url

@pytest.mark.parametrize("url", load_websites_from_yaml())
def test_availability(url):
    """Test if the website is reachable and returns status code 200."""
    try:
        response = fetch_url(url)
        assert response.status_code == 200, f"{url} is not available (status code: {response.status_code})"
    except Exception as e:
        pytest.fail(f"{url} failed due to an error: {e}")
