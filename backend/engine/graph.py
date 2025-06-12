from collections import defaultdict, deque
from typing import Dict, List, Set

from .models import GraphSpec

class GraphError(Exception):
    pass

class Graph:
    def __init__(self, graph_spec: GraphSpec):
        self.nodes = {node.id: node for node in graph_spec.nodes}
        self.adj: Dict[str, List[str]] = defaultdict(list)
        self.rev_adj: Dict[str, List[str]] = defaultdict(list)
        self.in_degree: Dict[str, int] = defaultdict(int)

        for edge in graph_spec.edges:
            from_node_id = edge.from_
            to_node_id = edge.to

            if from_node_id not in self.nodes:
                raise GraphError(f"Edge references non-existent node: {from_node_id}")
            if to_node_id not in self.nodes:
                raise GraphError(f"Edge references non-existent node: {to_node_id}")

            # Check for duplicate edges (optional, but good practice)
            if to_node_id not in self.adj[from_node_id]:
                self.adj[from_node_id].append(to_node_id)
                self.rev_adj[to_node_id].append(from_node_id)
                self.in_degree[to_node_id] += 1

        # Initialize in-degree for nodes with no incoming edges
        for node_id in self.nodes:
            if node_id not in self.in_degree:
                self.in_degree[node_id] = 0

    def get_node(self, node_id: str):
        return self.nodes.get(node_id)

    def get_dependencies(self, node_id: str) -> List[str]:
        """Returns the list of node IDs that this node depends on."""
        return self.rev_adj.get(node_id, [])

    def topological_sort(self) -> List[str]:
        """Performs topological sort using Kahn's algorithm."""
        queue = deque([node_id for node_id in self.nodes if self.in_degree[node_id] == 0])
        sorted_order: List[str] = []
        current_in_degree = self.in_degree.copy()

        while queue:
            u = queue.popleft()
            sorted_order.append(u)

            for v in self.adj[u]:
                current_in_degree[v] -= 1
                if current_in_degree[v] == 0:
                    queue.append(v)

        if len(sorted_order) != len(self.nodes):
            # Find nodes involved in the cycle
            visited = set()
            recursion_stack = set()
            cycle_nodes = set()

            def detect_cycle_util(node):
                visited.add(node)
                recursion_stack.add(node)

                for neighbor in self.adj[node]:
                    if neighbor not in visited:
                        if detect_cycle_util(neighbor):
                            cycle_nodes.add(node)
                            return True
                    elif neighbor in recursion_stack:
                        cycle_nodes.add(node)
                        cycle_nodes.add(neighbor)
                        # Trace back the cycle path if needed (more complex)
                        return True

                recursion_stack.remove(node)
                return False

            for node_id in self.nodes:
                if node_id not in visited:
                    if detect_cycle_util(node_id):
                        break # Stop once a cycle is detected

            raise GraphError(f"Graph contains a cycle. Involved nodes might include: {cycle_nodes}")

        return sorted_order 