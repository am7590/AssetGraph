import { BackendGraphSpec, BackendNodeSpec, BackendEdgeSpec, ValidationResult } from '../types/graph';
import { NODE_TYPE_MAPPING } from '../config/nodeTypeMapping';
import { NODE_PARAMETER_SCHEMAS } from '../config/parameterSchemas';

export class GraphValidator {
  static validateGraphSpec(graphSpec: BackendGraphSpec): ValidationResult {
    const errors: string[] = [];
    const warnings: string[] = [];

    // Validate nodes
    graphSpec.nodes.forEach((node, index) => {
      const nodeErrors = this.validateNode(node, index);
      errors.push(...nodeErrors);
    });

    // Validate edges
    graphSpec.edges.forEach((edge, index) => {
      const edgeErrors = this.validateEdge(edge, graphSpec.nodes, index);
      errors.push(...edgeErrors);
    });

    // Check for cycles
    if (this.hasCycles(graphSpec)) {
      errors.push('Graph contains cycles which may cause infinite execution');
    }

    // Check for disconnected nodes
    const disconnectedNodes = this.findDisconnectedNodes(graphSpec);
    if (disconnectedNodes.length > 0) {
      warnings.push(`Disconnected nodes found: ${disconnectedNodes.join(', ')}`);
    }

    return {
      isValid: errors.length === 0,
      errors,
      warnings
    };
  }

  private static validateNode(node: BackendNodeSpec, index: number): string[] {
    const errors: string[] = [];
    if (!node.id) errors.push(`Node ${index}: Missing id`);
    if (!node.type) errors.push(`Node ${index}: Missing type`);
    const validTypes = Object.values(NODE_TYPE_MAPPING);
    if (!validTypes.includes(node.type)) {
      errors.push(`Node ${index}: Invalid type '${node.type}'. Valid types: ${validTypes.join(', ')}`);
    }
    const schema = NODE_PARAMETER_SCHEMAS[node.type];
    if (schema) {
      schema.forEach(param => {
        if (param.required && !(param.name in node.params)) {
          errors.push(`Node ${index}: Missing required parameter '${param.name}'`);
        }
        if (param.name in node.params) {
          const value = node.params[param.name];
          if (param.type === 'number' && typeof value !== 'number') {
            errors.push(`Node ${index}: Parameter '${param.name}' must be a number`);
          }
          if (param.type === 'string' && typeof value !== 'string') {
            errors.push(`Node ${index}: Parameter '${param.name}' must be a string`);
          }
          if (param.type === 'boolean' && typeof value !== 'boolean') {
            errors.push(`Node ${index}: Parameter '${param.name}' must be a boolean`);
          }
        }
      });
    }
    return errors;
  }

  private static validateEdge(edge: BackendEdgeSpec, nodes: BackendNodeSpec[], index: number): string[] {
    const errors: string[] = [];
    if (!edge.from_) errors.push(`Edge ${index}: Missing from_ field`);
    if (!edge.to) errors.push(`Edge ${index}: Missing to field`);
    const nodeIds = nodes.map(n => n.id);
    if (!nodeIds.includes(edge.from_)) {
      errors.push(`Edge ${index}: Source node '${edge.from_}' does not exist`);
    }
    if (!nodeIds.includes(edge.to)) {
      errors.push(`Edge ${index}: Target node '${edge.to}' does not exist`);
    }
    return errors;
  }

  private static hasCycles(graphSpec: BackendGraphSpec): boolean {
    const visited = new Set<string>();
    const recStack = new Set<string>();
    const hasCycleDFS = (nodeId: string): boolean => {
      if (recStack.has(nodeId)) return true;
      if (visited.has(nodeId)) return false;
      visited.add(nodeId);
      recStack.add(nodeId);
      const outgoingEdges = graphSpec.edges.filter(e => e.from_ === nodeId);
      for (const edge of outgoingEdges) {
        if (hasCycleDFS(edge.to)) return true;
      }
      recStack.delete(nodeId);
      return false;
    };
    for (const node of graphSpec.nodes) {
      if (!visited.has(node.id)) {
        if (hasCycleDFS(node.id)) return true;
      }
    }
    return false;
  }

  private static findDisconnectedNodes(graphSpec: BackendGraphSpec): string[] {
    const connectedNodes = new Set<string>();
    graphSpec.edges.forEach(edge => {
      connectedNodes.add(edge.from_);
      connectedNodes.add(edge.to);
    });
    return graphSpec.nodes
      .map(node => node.id)
      .filter(id => !connectedNodes.has(id));
  }
} 