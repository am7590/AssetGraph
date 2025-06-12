from abc import ABC, abstractmethod
from typing import Any, Dict

class BaseNode(ABC):
    @abstractmethod
    def run(self, context: Dict[str, Any], params: Dict[str, Any]) -> Any:
        """Execute the node's logic."""
        pass 