import logging
import asyncio
from backend.utils.fmp_client import fetch_cash_flow_statement

logger = logging.getLogger(__name__)

# Define required state keys for this node
NODE_REQUIRES = ["current_ticker"]

def load_cash_flow_node(params):
    period = params.get("period", "annual")
    limit = params.get("limit", 5)

    async def node(state: dict) -> dict:
        node_name = "LoadCashFlow"
        current_errors = state.get("errors", []) # Get existing errors

        # --- Dependency Check ---
        missing_keys = [key for key in NODE_REQUIRES if key not in state or state[key] is None]
        if missing_keys:
            error_msg = f"Missing required state keys: {', '.join(missing_keys)}"
            logger.error(f"{node_name}: {error_msg}")
            # Return only the new error for this key
            return {"errors": current_errors + [f"{node_name}: {error_msg}"]}

        # --- Get Data from State ---
        ticker = state["current_ticker"] 
        
        logger.info(f"Running {node_name} for {ticker} (period={period}, limit={limit})")

        try:
            data = await fetch_cash_flow_statement(ticker, period=period, limit=limit)
            logger.info(f"Successfully fetched cash flow statement for {ticker}")
            # Return the successful state update (only the changed key)
            return {"raw_cash_flow": data}
        except Exception as e:
            error_msg = f"Failed to fetch cash flow statement for {ticker}: {e}"
            logger.error(f"{node_name}: {error_msg}")
            # Return only the new error
            return {"errors": current_errors + [f"{node_name}: {error_msg}"]}

    return node 