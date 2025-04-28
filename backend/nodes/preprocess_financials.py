import logging

logger = logging.getLogger(__name__)

def preprocess_financials_node(params):
    async def node(state: dict) -> dict:
        logger.info(f"Running PreprocessFinancials with params: {params}")
        current_errors = state.get("errors", [])
        processed_update = {}
        new_errors = []

        # --- Get Raw Data from State --- 
        # Relies on previous nodes populating these keys
        ticker_profile_list = state.get("ticker_profile")
        raw_income_statement = state.get("raw_income_statement")
        raw_balance_sheet = state.get("raw_balance_sheet")
        # raw_cash_flow = state.get("raw_cash_flow") # Not used in this example yet

        # --- Validate Inputs --- 
        if not raw_income_statement and not raw_balance_sheet:
            error_msg = "No raw income statement or balance sheet found in state for preprocessing."
            logger.warning(error_msg)
            new_errors.append(error_msg)
            # Return early if no essential data to process
            return {**state, "processed_financials": None, "errors": current_errors + [f"PreprocessFinancials: {e}" for e in new_errors]}

        # --- Preprocessing Logic (Example) --- 
        # TODO: Implement more sophisticated preprocessing/normalization
        try:
            processed_financials = {}

            # Extract latest annual income statement figures
            if isinstance(raw_income_statement, list) and raw_income_statement:
                latest_is = raw_income_statement[0] # FMP usually returns newest first
                processed_financials["latest_income_statement"] = {
                    "date": latest_is.get("date"),
                    "symbol": latest_is.get("symbol"),
                    "revenue": latest_is.get("revenue"),
                    "costOfRevenue": latest_is.get("costOfRevenue"),
                    "grossProfit": latest_is.get("grossProfit"),
                    "operatingExpenses": latest_is.get("operatingExpenses"),
                    "netIncome": latest_is.get("netIncome"),
                    # Add more fields as needed
                }
            else:
                logger.warning("No valid income statement data found for preprocessing.")
                new_errors.append("Income statement data missing or invalid format.")

            # Extract latest total assets and liabilities
            if isinstance(raw_balance_sheet, list) and raw_balance_sheet:
                latest_bs = raw_balance_sheet[0]
                processed_financials["latest_balance_sheet_summary"] = {
                    "date": latest_bs.get("date"),
                    "totalAssets": latest_bs.get("totalAssets"),
                    "totalLiabilities": latest_bs.get("totalLiabilities"),
                    "totalEquity": latest_bs.get("totalStockholdersEquity"),
                }
            else:
                logger.warning("No valid balance sheet data found for preprocessing.")
                new_errors.append("Balance sheet data missing or invalid format.")

            # Add profile info if available
            if isinstance(ticker_profile_list, list) and ticker_profile_list:
                ticker_profile = ticker_profile_list[0] # Extract dict from list
                if isinstance(ticker_profile, dict):
                    processed_financials["profile_summary"] = {
                        "symbol": ticker_profile.get("symbol"),
                        "companyName": ticker_profile.get("companyName"),
                        "sector": ticker_profile.get("sector"),
                        "industry": ticker_profile.get("industry"),
                    }
                else:
                     new_errors.append("Ticker profile item is not a dictionary.")
            else:
                 new_errors.append("Ticker profile data missing or invalid format.")

            processed_update["processed_financials"] = processed_financials
            if not new_errors: # Only log success if no new errors occurred here
                logger.info("Financials preprocessed.")

        except Exception as e:
            error_msg = f"Error during financial preprocessing: {e}"
            logger.exception(error_msg) # Log full traceback
            new_errors.append(error_msg)
            processed_update["processed_financials"] = None # Ensure it's None on error

        # --- Return Updated State --- 
        return {
            **state,
            **processed_update,
            "errors": current_errors + [f"PreprocessFinancials: {e}" for e in new_errors]
        }

    return node 