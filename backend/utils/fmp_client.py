import httpx
import os
from dotenv import load_dotenv
import logging

logger = logging.getLogger(__name__)
load_dotenv()

API_KEY = os.getenv("FMP_API_KEY")
BASE_URL = "https://financialmodelingprep.com/api/v3"

if not API_KEY:
    logger.error("FMP_API_KEY not found in environment variables.")
    raise ValueError("FMP_API_KEY not found in environment variables. Please set it in your .env file.")

async def _fetch_fmp(endpoint: str, params: dict = {}):
    """Helper function to fetch data from FMP API."""
    params["apikey"] = API_KEY
    url = f"{BASE_URL}/{endpoint}"
    async with httpx.AsyncClient(timeout=30.0) as client: # Add timeout
        try:
            logger.debug(f"Fetching FMP URL: {url} with params: {params}")
            response = await client.get(url, params=params)
            response.raise_for_status() # Raises HTTPStatusError for 4xx/5xx responses
            logger.debug(f"FMP Response Status: {response.status_code}")
            return response.json()
        except httpx.RequestError as exc:
            logger.error(f"An error occurred while requesting {exc.request.url!r}: {exc}")
            raise # Re-raise the exception to be handled by the caller node
        except httpx.HTTPStatusError as exc:
            logger.error(f"Error response {exc.response.status_code} while requesting {exc.request.url!r}: {exc.response.text}")
            raise # Re-raise the exception

async def fetch_company_profile(ticker: str):
    """Fetches company profile information."""
    endpoint = f"profile/{ticker}"
    return await _fetch_fmp(endpoint)

async def fetch_income_statement(ticker: str, period: str = "annual", limit: int = 5):
    """Fetches income statements."""
    endpoint = f"income-statement/{ticker}"
    params = {"period": period, "limit": limit}
    return await _fetch_fmp(endpoint, params)

async def fetch_balance_sheet(ticker: str, period: str = "annual", limit: int = 5):
    """Fetches balance sheet statements."""
    endpoint = f"balance-sheet-statement/{ticker}"
    params = {"period": period, "limit": limit}
    return await _fetch_fmp(endpoint, params)

async def fetch_cash_flow_statement(ticker: str, period: str = "annual", limit: int = 5):
    """Fetches cash flow statements."""
    endpoint = f"cash-flow-statement/{ticker}"
    params = {"period": period, "limit": limit}
    return await _fetch_fmp(endpoint, params) 