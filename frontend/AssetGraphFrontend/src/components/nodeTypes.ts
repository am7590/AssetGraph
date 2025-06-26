import { NodeTypes } from 'reactflow';
import CustomNode from './CustomNode';

// Create a frozen singleton instance
const nodeTypes: NodeTypes = Object.freeze({
  custom: CustomNode,
});

export default nodeTypes; 