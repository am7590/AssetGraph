import logging
import json

logger = logging.getLogger(__name__)

def generate_markdown_report_node(params):
    async def node(state: dict) -> dict:
        logger.info(f"Running GenerateMarkdownReport with params: {params}")
        current_errors = state.get("errors", [])
        report_update = {}
        new_errors = []

        # --- Get Data from State --- 
        processed_financials = state.get("processed_financials") or {}
        income_summary = state.get("income_summary")
        ticker = state.get("current_ticker")
        profile_summary = processed_financials.get("profile_summary", {})
        # You could also pull raw data here if needed for the report

        # --- Generate Report Content --- 
        try:
            report_components = []
            report_components.append("# Financial Report")

            company_name = profile_summary.get("companyName", ticker or "Unknown Company")
            report_components.append(f"\n## Company: {company_name} ({ticker or 'N/A'})")
            if profile_summary.get("sector") or profile_summary.get("industry"):
                report_components.append(f"Sector: {profile_summary.get('sector', 'N/A')} | Industry: {profile_summary.get('industry', 'N/A')}")

            # Include summary if available
            if income_summary:
                report_components.append("\n## Income Statement Summary")
                report_components.append(income_summary)
            else:
                 report_components.append("\n*No income statement summary was generated.*")

            # Include other processed data (example)
            bs_summary = processed_financials.get("latest_balance_sheet_summary")
            if bs_summary:
                report_components.append("\n## Balance Sheet Snapshot")
                bs_date = bs_summary.get("date", "Unknown Date")
                assets = bs_summary.get("totalAssets", "N/A")
                liabilities = bs_summary.get("totalLiabilities", "N/A")
                equity = bs_summary.get("totalEquity", "N/A")
                try: # Formatting
                    assets_f = f"{assets:,}" if assets != "N/A" else "N/A"
                    liab_f = f"{liabilities:,}" if liabilities != "N/A" else "N/A"
                    equity_f = f"{equity:,}" if equity != "N/A" else "N/A"
                except: assets_f, liab_f, equity_f = assets, liabilities, equity

                report_components.append(f"As of {bs_date}:\n" \
                                         f"- Total Assets: {assets_f}\n" \
                                         f"- Total Liabilities: {liab_f}\n" \
                                         f"- Total Equity: {equity_f}")

            # Include errors if any occurred during the *whole* process
            if current_errors:
                report_components.append("\n## Errors Encountered During Execution")
                for error in current_errors:
                    report_components.append(f"- `{error}`")

            report_content = "\n".join(report_components)
            report_update["markdown_report"] = report_content
            logger.info(f"Markdown report generated for {ticker}.")

        except Exception as e:
            error_msg = f"Error generating markdown report: {e}"
            logger.exception(error_msg)
            new_errors.append(error_msg)
            report_update["markdown_report"] = f"# Report Generation Failed\n\nError: {error_msg}"

        # --- Return Updated State --- 
        # Note: We keep the original errors list (`current_errors`) and add any *new* errors
        # from this specific node (`new_errors`)
        return {
            **state,
            **report_update,
            "errors": current_errors + [f"GenerateMarkdownReport: {e}" for e in new_errors]
        }

    return node 