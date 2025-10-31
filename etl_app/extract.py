import logging
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

logger = logging.getLogger(__name__)

API_URL = "https://restcountries.com/v3.1/all?fields=name,flags,population,tld,currencies,capital,languages,area,borders,timezones"


def get_session_with_retries():
    """
    Create and configure a requests session with automatic retries.

    The session retries failed requests up to 3 times with exponential backoff
    for specific HTTP status codes (500, 502, 503, 504).

    Returns:
        requests.Session: Configured session object with retry logic.
    """
    session = requests.Session()
    retries = Retry(total=3, backoff_factor=2, status_forcelist=[500, 502, 503, 504])
    session.mount("https://", HTTPAdapter(max_retries=retries))
    return session


def extract_countries(session, api_url=API_URL, timeout=60):
    """
    Fetch raw country data from the REST Countries API.

    Returns:
        list[dict]: List of country records as dictionaries.
    """
    logger.info("Fetching countries from REST Countries API...")

    resp = session.get(api_url, timeout=timeout)
    resp.raise_for_status()

    logger.info("Succesfully fetched countries from API.")
    return resp.json()