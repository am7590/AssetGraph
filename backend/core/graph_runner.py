import operator # Import operator
from typing import Dict, Any, Optional, List
from typing_extensions import TypedDict, Annotated
from langgraph.channels import LastValue
from backend.models.graph_spec import GraphSpec
from langgraph.graph import StateGraph
from backend.nodes.load_ticker_data import load_ticker_data_node
from backend.nodes.load_income_statement import load_income_statement_node
from backend.nodes.load_balance_sheet import load_balance_sheet_node
from backend.nodes.load_cash_flow import load_cash_flow_node
from backend.nodes.preprocess_financials import preprocess_financials_node
from backend.nodes.summarize_income_statement import summarize_income_statement_node
from backend.nodes.generate_llm_report import generate_llm_report_node

# Define the state schema for the graph
class GraphState(TypedDict):
    # Ticker being processed - Use Annotated LastValue for concurrency
    current_ticker: Annotated[Optional[str], LastValue]
    # Raw profile data fetched for the ticker (FMP returns list)
    # Annotate potentially concurrent writes, even if to distinct keys within the step
    ticker_profile: Annotated[Optional[List[Dict[str, Any]]], LastValue]
    # Raw financial statements (FMP returns list)
    raw_income_statement: Annotated[Optional[List[Dict[str, Any]]], LastValue]
    raw_balance_sheet: Annotated[Optional[List[Dict[str, Any]]], LastValue]
    raw_cash_flow: Annotated[Optional[List[Dict[str, Any]]], LastValue]
    # Processed financial data (example: structure as needed)
    processed_financials: Annotated[Optional[Dict[str, Any]], LastValue]
    # Text summary of income statement
    income_summary: Annotated[Optional[str], LastValue]
    # Final markdown report content
    markdown_report: Annotated[Optional[str], LastValue]
    # List to accumulate errors from nodes - Use operator.add reducer
    errors: Annotated[List[str], operator.add]

NODE_TYPE_MAPPING = {
    "LoadTickerData": load_ticker_data_node,
    "LoadIncomeStatement": load_income_statement_node,
    "LoadBalanceSheet": load_balance_sheet_node,
    "LoadCashFlow": load_cash_flow_node,
    "PreprocessFinancials": preprocess_financials_node,
    "SummarizeIncomeStatement": summarize_income_statement_node,
    "GenerateLLMReport": generate_llm_report_node
}

async def run_graph(graph_spec: GraphSpec):
    # Pass the state schema to StateGraph
    builder = StateGraph(GraphState)

    node_instances = {}

    # Instantiate nodes based on spec
    for node_spec in graph_spec.nodes:
        node_factory = NODE_TYPE_MAPPING.get(node_spec.type)
        if not node_factory:
            raise ValueError(f"Unknown node type: {node_spec.type}")
        # Pass params to the node factory function to get the actual node function
        node_function = node_factory(node_spec.params)
        # Add node to the graph builder
        builder.add_node(node_spec.id, node_function)

    # Add edges based on spec
    for edge_spec in graph_spec.edges:
        builder.add_edge(edge_spec.from_, edge_spec.to)

    # Set the entry point
    if graph_spec.nodes:
        builder.set_entry_point(graph_spec.nodes[0].id)
    else:
        raise ValueError("GraphSpec must contain at least one node.")

    # Build the graph
    graph = builder.compile()

    # Invoke the graph with an initial empty state
    # Initialize the errors list
    initial_state = {"errors": []}
    result = await graph.ainvoke(initial_state)
    return result
