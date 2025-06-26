import { Node } from 'reactflow';

export class LayoutManager {
  private static readonly NODE_WIDTH = 200;
  private static readonly NODE_HEIGHT = 100;
  private static readonly HORIZONTAL_SPACING = 250;
  private static readonly VERTICAL_SPACING = 150;

  static assignPositions(nodes: Node[], edges: any[]): Node[] {
    // Simple grid layout for imported graphs
    const nodesPerRow = Math.ceil(Math.sqrt(nodes.length));
    return nodes.map((node, index) => ({
      ...node,
      position: {
        x: (index % nodesPerRow) * this.HORIZONTAL_SPACING,
        y: Math.floor(index / nodesPerRow) * this.VERTICAL_SPACING
      }
    }));
  }

  static preservePositions(nodes: Node[]): Record<string, { x: number, y: number }> {
    const positions: Record<string, { x: number, y: number }> = {};
    nodes.forEach(node => {
      positions[node.id] = { x: node.position.x, y: node.position.y };
    });
    return positions;
  }

  static restorePositions(nodes: Node[], positions: Record<string, { x: number, y: number }>): Node[] {
    return nodes.map(node => ({
      ...node,
      position: positions[node.id] || { x: 0, y: 0 }
    }));
  }
} 