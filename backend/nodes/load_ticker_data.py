import logging
import asyncio
from backend.utils.fmp_client import fetch_company_profile

logger = logging.getLogger(__name__)

def load_ticker_data_node(params):

    async def node(state: dict) -> dict:
        ticker = params.get("ticker") # Ticker comes from params for the first node
        # No need to get current_errors anymore
        node_name = "LoadTickerData"

        if not ticker:
            error_msg = f"Ticker parameter missing for {node_name}"
            logger.error(error_msg)
            # Return only the new error for this key
            return {"errors": [f"{node_name}: {error_msg}"]}

        logger.info(f"Running {node_name} for {ticker}")

        try:
            profile_data = await fetch_company_profile(ticker)
            logger.info(f"Successfully fetched profile for {ticker}")
            # Return the successful state update
            return {"ticker_profile": profile_data, "current_ticker": ticker}
        except Exception as e:
            error_msg = f"Failed to fetch profile for {ticker}: {e}"
            logger.error(error_msg)
            # Return ticker (so other nodes can run) and the new error
            return {"current_ticker": ticker, "errors": [f"{node_name}: {error_msg}"]}

    return node
