import logging

logger = logging.getLogger(__name__)

# Define required state keys for this node
NODE_REQUIRES = ["processed_financials"]

def summarize_income_statement_node(params):
    async def node(state: dict) -> dict:
        node_name = "SummarizeIncomeStatement"
        logger.info(f"Running {node_name} with params: {params}")
        current_errors = state.get("errors", [])
        new_errors = []

        # --- Dependency Check ---
        missing_keys = [key for key in NODE_REQUIRES if key not in state or state[key] is None]
        if missing_keys:
            error_msg = f"Missing required state keys: {', '.join(missing_keys)}"
            logger.error(f"{node_name}: {error_msg}")
            return {"income_summary": None, "errors": current_errors + [f"{node_name}: {error_msg}"]}

        # --- Get Data from State --- 
        processed_financials = state["processed_financials"]
        summary_update = {}

        # --- Validate Input Format/Content --- 
        if not isinstance(processed_financials, dict):
            error_msg = "Processed financials data invalid format (expected dict)."
            logger.warning(f"{node_name}: {error_msg}")
            new_errors.append(error_msg)
            summary_update["income_summary"] = None
            return {**summary_update, "errors": current_errors + [f"{node_name}: {e}" for e in new_errors]}

        latest_is = processed_financials.get("latest_income_statement")
        if not latest_is or not isinstance(latest_is, dict):
             error_msg = "latest_income_statement not found or invalid in processed_financials."
             logger.warning(f"{node_name}: {error_msg}")
             new_errors.append(error_msg)
             summary_update["income_summary"] = None
             # Return only the updates (summary and errors)
             return {**summary_update, "errors": current_errors + [f"{node_name}: {e}" for e in new_errors]}

        # --- Summarization Logic (Placeholder - No LLM yet) --- 
        # TODO: Replace with actual LLM call for summarization
        try:
            # Create a simple summary string from the extracted data
            revenue = latest_is.get("revenue", "N/A")
            gross_profit = latest_is.get("grossProfit", "N/A")
            net_income = latest_is.get("netIncome", "N/A")
            summary_date = latest_is.get("date", "Unknown Date")

            # Format numbers for readability (optional)
            try:
                revenue_f = f"{revenue:,}" if revenue != "N/A" else "N/A"
                gp_f = f"{gross_profit:,}" if gross_profit != "N/A" else "N/A"
                ni_f = f"{net_income:,}" if net_income != "N/A" else "N/A"
            except (ValueError, TypeError):
                 revenue_f, gp_f, ni_f = revenue, gross_profit, net_income # Fallback if formatting fails

            summary = (
                f"For the period ending {summary_date}:\n"
                f"- Revenue: {revenue_f}\n"
                f"- Gross Profit: {gp_f}\n"
                f"- Net Income: {ni_f}"
            )
            summary_update["income_summary"] = summary
            logger.info("Income statement summarized (rule-based).")

        except Exception as e:
            error_msg = f"Error during income statement summarization: {e}"
            logger.exception(error_msg)
            new_errors.append(error_msg)
            summary_update["income_summary"] = None

        # --- Return Updated State --- 
        # Return only the updates (summary and errors)
        return {
            **summary_update,
            "errors": current_errors + [f"{node_name}: {e}" for e in new_errors]
        }

    return node 