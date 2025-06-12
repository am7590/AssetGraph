import json
import logging
import sys
from pathlib import Path

# Ensure the backend directory is in the Python path
project_root = Path(__file__).parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from backend.engine.execution_engine import ExecutionEngine
from backend.engine.models import GraphSpec

# --- Configuration ---
LOG_LEVEL = logging.INFO
EXAMPLE_GRAPH = {
  "nodes": [
    { "id": "load_aapl", "type": "Load10K", "params": {"ticker": "AAPL"} },
    { "id": "load_msft", "type": "Load10K", "params": {"ticker": "MSFT"} },
    { "id": "summarize_aapl", "type": "Summarize10K", "params": {} },
    { "id": "summarize_msft", "type": "Summarize10K", "params": {} },
    { "id": "final_step", "type": "Summarize10K", "params": {} } # Reusing Summarize just for demo
  ],
  "edges": [
    { "from": "load_aapl", "to": "summarize_aapl" },
    { "from": "load_msft", "to": "summarize_msft" },
    # Edges to final_step to demonstrate multiple dependencies
    { "from": "summarize_aapl", "to": "final_step" },
    { "from": "summarize_msft", "to": "final_step" }
  ]
}

# Example with a cycle (should raise an error)
CYCLIC_GRAPH = {
    "nodes": [
        { "id": "n1", "type": "Load10K", "params": {}},
        { "id": "n2", "type": "Summarize10K", "params": {}},
        { "id": "n3", "type": "Load10K", "params": {}}
    ],
    "edges": [
        { "from": "n1", "to": "n2" },
        { "from": "n2", "to": "n3" },
        { "from": "n3", "to": "n1" } # Cycle!
    ]
}

# Example with missing node type
MISSING_TYPE_GRAPH = {
    "nodes": [
        { "id": "n1", "type": "Load10K", "params": {}},
        { "id": "n2", "type": "NonExistentNode", "params": {}}
    ],
    "edges": [
        { "from": "n1", "to": "n2" }
    ]
}

# --- Logging Setup ---
logging.basicConfig(level=LOG_LEVEL,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    handlers=[logging.StreamHandler()])
logger = logging.getLogger(__name__)

# --- Main Execution ---
def main():
    logger.info("Initializing Execution Engine...")
    # Set reload_nodes=True if you want it to re-scan the nodes folder on every run
    engine = ExecutionEngine(reload_nodes=True)

    logger.info("--- Running Example Graph ---")
    try:
        graph_spec = GraphSpec(**EXAMPLE_GRAPH)
        results = engine.run(graph_spec)
        logger.info("Example Graph Results:")
        print(json.dumps({k: v.dict() for k, v in results.items()}, indent=2))
    except Exception as e:
        logger.error(f"Error running example graph: {e}", exc_info=True)

    # print("\n---")

    # logger.info("--- Running Cyclic Graph (expecting error) ---")
    # try:
    #     cyclic_graph_spec = GraphSpec(**CYCLIC_GRAPH)
    #     results_cyclic = engine.run(cyclic_graph_spec)
    #     logger.info("Cyclic Graph Results (should not reach here often):")
    #     print(json.dumps({k: v.dict() for k, v in results_cyclic.items()}, indent=2))
    # except Exception as e:
    #     logger.error(f"Successfully caught error in cyclic graph: {e}")

    # print("\n---")

    # logger.info("--- Running Graph with Missing Node Type (expecting error) ---")
    # try:
    #     missing_type_spec = GraphSpec(**MISSING_TYPE_GRAPH)
    #     results_missing = engine.run(missing_type_spec)
    #     logger.info("Missing Type Graph Results:")
    #     print(json.dumps({k: v.dict() for k, v in results_missing.items()}, indent=2))
    # except Exception as e:
    #     logger.error(f"Successfully caught error for missing node type: {e}")

if __name__ == "__main__":
    main() 