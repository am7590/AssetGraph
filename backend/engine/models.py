from pydantic import BaseModel, Field
from typing import Any, Dict, List, Optional

class NodeResult(BaseModel):
    status: str = "pending"  # "pending", "running", "done", "error"
    result: Any = None
    error: Optional[str] = None

class NodeSpec(BaseModel):
    id: str
    type: str
    params: Dict[str, Any] = Field(default_factory=dict)
    # 'depends_on' is implicitly handled by edges, but keeping it for potential future use/clarity
    # depends_on: List[str] = Field(default_factory=list)

class EdgeSpec(BaseModel):
    from_: str = Field(..., alias='from') # Alias 'from' because it's a Python keyword
    to: str

class GraphSpec(BaseModel):
    nodes: List[NodeSpec]
    edges: List[EdgeSpec] 