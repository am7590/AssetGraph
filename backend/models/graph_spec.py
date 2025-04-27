from typing import List, Dict, Any
from pydantic import BaseModel

class NodeSpec(BaseModel):
    id: str
    type: str
    params: Dict[str, Any] = {}

class EdgeSpec(BaseModel):
    from_: str
    to: str

class GraphSpec(BaseModel):
    nodes: List[NodeSpec]
    edges: List[EdgeSpec]
