import logging

logger = logging.getLogger(__name__)

def preprocess_financials_node(params):
    async def node(state: dict) -> dict:
        logger.info(f"Preprocessing financials with params: {params}")
        current_errors = state.get("errors", [])
        ticker_data = state.get("ticker_data") # Get None if not present

        if not ticker_data:
            error_msg = "No ticker_data found in state for preprocessing."
            logger.warning(error_msg)
            # Add error to state and return
            return {**state, "preprocessed_financials": None, "errors": current_errors + [f"PreprocessFinancials: {error_msg}"]}

        # TODO: Implement actual preprocessing logic
        # Example: Placeholder processing
        try:
            # Simulate processing - replace with real logic
            processed_data = {"processed": True, "original_keys": list(ticker_data.keys())}
            logger.info("Financials preprocessed (placeholder)")
            return {**state, "preprocessed_financials": processed_data}
        except Exception as e:
            error_msg = f"Error during financial preprocessing: {e}"
            logger.error(error_msg)
            return {**state, "preprocessed_financials": None, "errors": current_errors + [f"PreprocessFinancials: {error_msg}"]}

    return node 