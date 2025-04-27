import httpx
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("FMP_API_KEY")

if not API_KEY:
    raise ValueError("FMP_API_KEY not found in environment variables. Please set it in your .env file.")

async def fetch_company_profile(ticker: str):
    url = f"https://financialmodelingprep.com/api/v3/profile/{ticker}?apikey={API_KEY}"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        if response.status_code != 200:
            response.raise_for_status()
        return response.json() 