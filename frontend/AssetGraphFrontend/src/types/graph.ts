export interface Node {
  id: string;
  type: string;
  params: Record<string, any>;
}

export interface Edge {
  from_: string;
  to: string;
}

export interface GraphNode {
  id: string;
  type: string;
  params: Record<string, any>;
}

export interface GraphEdge {
  from_: string;
  to: string;
}

export interface GraphSpec {
  nodes: GraphNode[];
  edges: GraphEdge[];
}

export interface GraphResult {
  [key: string]: {
    status: string;
    output?: any;
    error?: string;
  };
}

// Backend-compatible types
export interface BackendNodeSpec {
  id: string;
  type: string;
  params: Record<string, any>;
}

export interface BackendEdgeSpec {
  from_: string;
  to: string;
}

export interface BackendGraphSpec {
  nodes: BackendNodeSpec[];
  edges: BackendEdgeSpec[];
}

// Frontend extended types (includes position data)
export interface FrontendGraphData {
  nodes: BackendNodeSpec[];
  edges: BackendEdgeSpec[];
  positions?: Record<string, { x: number, y: number }>;
  metadata?: {
    version: string;
    created: string;
    lastModified: string;
  };
}

// Validation result type
export interface ValidationResult {
  isValid: boolean;
  errors: string[];
  warnings: string[];
} 