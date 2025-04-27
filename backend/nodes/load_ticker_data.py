import logging
from backend.utils.fmp_client import fetch_company_profile

logger = logging.getLogger(__name__)

def load_ticker_data_node(params):
    async def node(state: dict) -> dict:
        ticker = params.get("ticker")
        current_errors = state.get("errors", [])

        if not ticker:
            error_msg = "Ticker parameter missing for LoadTickerData node"
            logger.error(error_msg)
            # Add error to state and return
            return {**state, "errors": current_errors + [f"LoadTickerData: {error_msg}"]}

        logger.info(f"Loading data for ticker: {ticker} with params: {params}")
        try:
            # Example: Fetch profile data
            profile_data = await fetch_company_profile(ticker)
            logger.info(f"Successfully fetched data for {ticker}")
            # Update the state successfully
            return {**state, "ticker_data": profile_data, "current_ticker": ticker}
        except Exception as e:
            error_msg = f"Error fetching data for {ticker}: {e}"
            logger.error(error_msg)
            # Add error to state and return
            return {**state, "errors": current_errors + [f"LoadTickerData: {error_msg}"]}

    return node
