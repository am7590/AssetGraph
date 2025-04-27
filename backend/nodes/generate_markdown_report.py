import logging
import json

logger = logging.getLogger(__name__)

def generate_markdown_report_node(params):
    async def node(state: dict) -> dict:
        logger.info(f"Generating markdown report with params: {params}")
        current_errors = state.get("errors", [])

        # Create a report based on the state, including errors
        try:
            report_components = []
            report_components.append("# Financial Report")

            if state.get("current_ticker"):
                report_components.append(f"\n## Ticker: {state['current_ticker']}")

            # Include summary if available
            income_summary = state.get("income_summary")
            if income_summary:
                report_components.append("\n## Income Statement Summary")
                report_components.append(income_summary)
            else:
                 report_components.append("\n*No income statement summary generated.*")

            # Include errors if any occurred
            if current_errors:
                report_components.append("\n## Errors Encountered")
                for error in current_errors:
                    report_components.append(f"- `{error}`")

            # Placeholder for further data
            # report_components.append("\n## Raw Data (Excerpt)")
            # report_components.append(f"```json\n{json.dumps(state.get('ticker_data', {}), indent=2)[:500]}...\n```")

            report_content = "\n".join(report_components)
            logger.info("Markdown report generated.")
            # We don't add to errors here, just return the report content
            # Keep the existing errors list in the state
            return {**state, "markdown_report": report_content}

        except Exception as e:
            # Catch errors during report generation itself
            error_msg = f"Error generating markdown report: {e}"
            logger.error(error_msg)
            # Add this specific error to the list
            final_errors = current_errors + [f"GenerateMarkdownReport: {error_msg}"]
            # Return minimal state with the error
            return {**state, "markdown_report": f"# Report Generation Failed\n\nError: {error_msg}", "errors": final_errors}

    return node 