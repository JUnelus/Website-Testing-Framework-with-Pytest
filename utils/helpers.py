# helpers.py
import yaml
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


def load_websites_from_yaml(file_path=r'C:\Users\big_j\PycharmProjects\Website-Testing-Framework-with-Pytest\websites.yaml'):
    """Loads website URLs from the YAML file."""
    with open(file_path, 'r') as file:
        config = yaml.safe_load(file)
    return config['websites']


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
