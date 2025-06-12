import logging
from typing import Any, Dict

from .graph import Graph, GraphError
from .models import GraphSpec, NodeResult
from .node_loader import NodeLoaderError, get_node_class, reload_node_classes

logger = logging.getLogger(__name__)

class ExecutionEngine:
    def __init__(self, reload_nodes: bool = False):
        """Initializes the ExecutionEngine.

        Args:
            reload_nodes: If True, forces reloading of node classes on each run.
                          Useful for development environments.
        """
        self.reload_nodes = reload_nodes

    def run(self, graph_spec: GraphSpec) -> Dict[str, NodeResult]:
        """Executes the graph defined by the GraphSpec."""
        if self.reload_nodes:
            reload_node_classes() # Reload classes if requested

        logger.info("Starting graph execution.")
        try:
            graph = Graph(graph_spec)
            sorted_node_ids = graph.topological_sort()
            logger.info(f"Execution order: {sorted_node_ids}")
        except (GraphError, NodeLoaderError) as e:
            logger.error(f"Graph validation failed: {e}")
            # Return results indicating the error occurred before execution started
            results = {node.id: NodeResult(status="error", error=f"Graph validation failed: {e}")
                       for node in graph_spec.nodes}
            return results
        except Exception as e:
            logger.error(f"Unexpected error during graph initialization: {e}", exc_info=True)
            results = {node.id: NodeResult(status="error", error=f"Unexpected error during graph initialization: {e}")
                       for node in graph_spec.nodes}
            return results

        context: Dict[str, Any] = {}
        results: Dict[str, NodeResult] = {node_id: NodeResult() for node_id in graph.nodes}

        for node_id in sorted_node_ids:
            node_spec = graph.get_node(node_id)
            if not node_spec:
                 # This shouldn't happen if graph validation is correct, but defensive check
                 logger.error(f"Node ID {node_id} from sorted list not found in graph.")
                 results[node_id] = NodeResult(status="error", error="Node definition not found during execution")
                 continue

            results[node_id].status = "running"
            logger.info(f"Running node '{node_id}' (Type: {node_spec.type})")

            try:
                # Get node class dynamically
                NodeClass = get_node_class(node_spec.type)
                node_instance = NodeClass()

                # Prepare context for the current node (results of dependencies)
                node_context = {}
                dependencies = graph.get_dependencies(node_id)
                for dep_id in dependencies:
                    if results[dep_id].status == "done":
                        node_context[dep_id] = results[dep_id].result
                    else:
                        # This indicates an issue, as dependencies should be 'done'
                        error_msg = f"Dependency '{dep_id}' did not complete successfully (status: {results[dep_id].status})."
                        logger.error(f"Node '{node_id}': {error_msg} Error: {results[dep_id].error}")
                        raise RuntimeError(error_msg)

                # Execute the node's run method
                node_result_data = node_instance.run(context=node_context, params=node_spec.params)

                # Update context and results
                context[node_id] = node_result_data
                results[node_id].result = node_result_data
                results[node_id].status = "done"
                logger.info(f"Node '{node_id}' finished successfully.")

            except NodeLoaderError as e:
                error_msg = f"Failed to load node class: {e}"
                logger.error(f"Node '{node_id}': {error_msg}", exc_info=True)
                results[node_id].status = "error"
                results[node_id].error = error_msg
                # Optional: Decide if the entire graph execution should stop on error
                # For now, we continue, but subsequent nodes might fail if they depend on this one.

            except Exception as e:
                error_msg = f"Execution failed: {e}"
                logger.error(f"Node '{node_id}': {error_msg}", exc_info=True)
                results[node_id].status = "error"
                results[node_id].error = error_msg
                # Optional: Stop execution globally on node error?
                # break # Uncomment to stop execution on the first error

        logger.info("Graph execution finished.")
        return results 