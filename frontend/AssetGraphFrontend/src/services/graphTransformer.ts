import { Node, Edge } from 'reactflow';
import { BackendGraphSpec, BackendNodeSpec, BackendEdgeSpec, FrontendGraphData } from '../types/graph';
import { NODE_TYPE_MAPPING, BACKEND_TO_FRONTEND_MAPPING } from '../config/nodeTypeMapping';
import { NODE_PARAMETER_SCHEMAS } from '../config/parameterSchemas';
import { LayoutManager } from '../utils/layoutManager';
import { GraphValidator } from './graphValidator';

export class GraphTransformer {
  static toBackendFormat(nodes: Node[], edges: Edge[]): BackendGraphSpec {
    const backendNodes = nodes.map(node => this.transformNode(node));
    const backendEdges = edges.map(edge => this.transformEdge(edge));
    return {
      nodes: backendNodes,
      edges: backendEdges
    };
  }

  static fromBackendFormat(graphSpec: BackendGraphSpec, positions?: Record<string, { x: number, y: number }>): { nodes: Node[], edges: Edge[] } {
    // Validate before transformation
    const validation = GraphValidator.validateGraphSpec(graphSpec);
    if (!validation.isValid) {
      throw new Error(`Invalid graph specification: ${validation.errors.join(', ')}`);
    }
    if (validation.warnings.length > 0) {
      console.warn('Graph validation warnings:', validation.warnings);
    }
    const nodes = graphSpec.nodes.map(node => this.transformBackendNode(node));
    const edges = graphSpec.edges.map(edge => this.transformBackendEdge(edge));
    // Apply positions if provided, otherwise use layout manager
    const positionedNodes = positions
      ? LayoutManager.restorePositions(nodes, positions)
      : LayoutManager.assignPositions(nodes, edges);
    return {
      nodes: positionedNodes,
      edges
    };
  }

  static toFrontendFormat(nodes: Node[], edges: Edge[]): FrontendGraphData {
    const backendSpec = this.toBackendFormat(nodes, edges);
    const positions = LayoutManager.preservePositions(nodes);
    return {
      nodes: backendSpec.nodes,
      edges: backendSpec.edges,
      positions,
      metadata: {
        version: '1.0.0',
        created: new Date().toISOString(),
        lastModified: new Date().toISOString()
      }
    };
  }

  private static transformNode(node: Node): BackendNodeSpec {
    // Ensure type mapping is applied
    const backendType = NODE_TYPE_MAPPING[node.data.type] || node.data.type;
    // Apply parameter defaults
    const schema = NODE_PARAMETER_SCHEMAS[backendType];
    const params = { ...node.data.params };
    if (schema) {
      schema.forEach(param => {
        if (!(param.name in params) && param.default !== undefined) {
          params[param.name] = param.default;
        }
      });
    }
    return {
      id: node.id,
      type: backendType,
      params
    };
  }

  private static transformEdge(edge: Edge): BackendEdgeSpec {
    return {
      from_: edge.source,
      to: edge.target
    };
  }

  private static transformBackendNode(node: BackendNodeSpec): Node {
    const frontendType = BACKEND_TO_FRONTEND_MAPPING[node.type] || node.type;
    return {
      id: node.id,
      type: 'custom',
      position: { x: 0, y: 0 }, // Will be set by layout manager
      data: {
        type: frontendType,
        label: this.getNodeLabel(frontendType),
        params: node.params
      }
    };
  }

  private static transformBackendEdge(edge: BackendEdgeSpec): Edge {
    return {
      id: `${edge.from_}-${edge.to}`,
      source: edge.from_,
      target: edge.to,
      type: 'smoothstep',
      animated: true
    };
  }

  private static getNodeLabel(type: string): string {
    // This would come from your existing NODE_CONFIGS
    const configs = {
      'LoadTickerData': 'Load Ticker Data',
      'LoadIncomeStatement': 'Load Income Statement',
      'LoadBalanceSheet': 'Load Balance Sheet',
      'LoadCashFlow': 'Load Cash Flow',
      'PreprocessFinancials': 'Preprocess Financials',
      'SummarizeIncomeStatement': 'Summarize Income Statement',
      'GenerateLLMReport': 'Generate LLM Report'
    };
    return configs[type] || type;
  }
} 