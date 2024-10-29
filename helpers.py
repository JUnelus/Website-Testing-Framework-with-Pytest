import os
import yaml
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


def load_websites_from_yaml():
    # Check if 'websites.yaml' is in the current or parent directory
    file_path = os.path.join(os.path.dirname(__file__), 'websites.yaml')
    if not os.path.exists(file_path):
        # Try finding it in the root directory
        file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'websites.yaml')
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Cannot find websites.yaml at {file_path}")

    with open(file_path, 'r') as file:
        websites = yaml.safe_load(file)
    return websites


def fetch_url(url, retries=3, timeout=20):
    """Fetches the content of a URL with retries and custom headers."""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36'
    }

    session = requests.Session()
    retry_strategy = Retry(
        total=retries,
        backoff_factor=2,
        status_forcelist=[403, 429, 500, 502, 503, 504]
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("http://", adapter)
    session.mount("https://", adapter)

    response = session.get(url, headers=headers, timeout=timeout)
    response.raise_for_status()
    return response
