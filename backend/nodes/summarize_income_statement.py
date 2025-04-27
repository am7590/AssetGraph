import logging

logger = logging.getLogger(__name__)

def summarize_income_statement_node(params):
    async def node(state: dict) -> dict:
        logger.info(f"Summarizing income statement with params: {params}")
        current_errors = state.get("errors", [])
        preprocessed_data = state.get("preprocessed_financials") # Get None if not present

        if not preprocessed_data:
            error_msg = "No preprocessed_financials found in state for summarization."
            logger.warning(error_msg)
            # Add error to state and return
            return {**state, "income_summary": None, "errors": current_errors + [f"SummarizeIncomeStatement: {error_msg}"]}

        # TODO: Implement actual summarization logic (likely using an LLM)
        # Example: Placeholder summary
        try:
            # Simulate summarization - replace with real logic
            summary = f"Placeholder summary of income statement based on data: {str(preprocessed_data)[:100]}..."
            logger.info("Income statement summarized (placeholder)")
            return {**state, "income_summary": summary}
        except Exception as e:
            error_msg = f"Error during income statement summarization: {e}"
            logger.error(error_msg)
            return {**state, "income_summary": None, "errors": current_errors + [f"SummarizeIncomeStatement: {error_msg}"]}

    return node 