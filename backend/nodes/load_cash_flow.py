import logging
import asyncio
from backend.utils.fmp_client import fetch_cash_flow_statement

logger = logging.getLogger(__name__)

def load_cash_flow_node(params):
    period = params.get("period", "annual")
    limit = params.get("limit", 5)

    async def node(state: dict) -> dict:
        ticker = state.get("current_ticker")
        current_errors = state.get("errors", [])
        node_name = "LoadCashFlow"

        if not ticker:
            error_msg = f"Ticker not found in state for {node_name}"
            logger.error(error_msg)
            return {**state, "errors": current_errors + [f"{node_name}: {error_msg}"]}

        logger.info(f"Running {node_name} for {ticker} (period={period}, limit={limit})")

        try:
            data = await fetch_cash_flow_statement(ticker, period=period, limit=limit)
            logger.info(f"Successfully fetched cash flow statement for {ticker}")
            return {**state, "raw_cash_flow": data}
        except Exception as e:
            error_msg = f"Failed to fetch cash flow statement for {ticker}: {e}"
            logger.error(error_msg)
            return {**state, "errors": current_errors + [f"{node_name}: {error_msg}"]}

    return node 