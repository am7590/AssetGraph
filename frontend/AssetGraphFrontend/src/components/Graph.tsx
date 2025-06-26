import React, { useState, useCallback, useRef, useEffect } from 'react';
import ReactFlow, {
  Background,
  Controls,
  MiniMap,
  useNodesState,
  useEdgesState,
  addEdge,
  Connection,
  Edge,
  Node,
  Panel,
} from 'reactflow';
import 'reactflow/dist/style.css';
import nodeTypes from './nodeTypes';
import { executeGraph } from '../services/graphService';
import { NODE_CONFIGS } from '../config/nodeConfigs';
import { GraphTransformer } from '../services/graphTransformer';

interface GraphProps {
  onGenerateJson: (nodes: Node[], edges: Edge[]) => void;
  initialNodes?: Node[];
  initialEdges?: Edge[];
}

export function Graph({ onGenerateJson, initialNodes = [], initialEdges = [] }: GraphProps) {
  const reactFlowWrapper = useRef<HTMLDivElement>(null);
  const [nodes, setNodes, onNodesChange] = useNodesState(initialNodes);
  const [edges, setEdges, onEdgesChange] = useEdgesState(initialEdges);
  const [reactFlowInstance, setReactFlowInstance] = useState<any>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Keep parent component updated with current nodes and edges
  useEffect(() => {
    onGenerateJson(nodes, edges);
  }, [nodes, edges, onGenerateJson]);

  // Update nodes and edges when initialNodes or initialEdges change
  useEffect(() => {
    setNodes(initialNodes);
    setEdges(initialEdges);
  }, [initialNodes, initialEdges, setNodes, setEdges]);

  const onConnect = useCallback(
    (params: Connection) => setEdges((eds) => addEdge(params, eds)),
    [setEdges]
  );

  const onDragOver = useCallback((event: React.DragEvent<HTMLDivElement>) => {
    event.preventDefault();
    event.dataTransfer.dropEffect = 'move';
  }, []);

  const onDrop = useCallback(
    (event: React.DragEvent<HTMLDivElement>) => {
      event.preventDefault();

      if (!reactFlowWrapper.current || !reactFlowInstance) return;

      const reactFlowBounds = reactFlowWrapper.current.getBoundingClientRect();
      const type = event.dataTransfer.getData('application/reactflow');
      const nodeConfig = NODE_CONFIGS[type];

      if (!nodeConfig) return;

      const position = reactFlowInstance.project({
        x: event.clientX - reactFlowBounds.left,
        y: event.clientY - reactFlowBounds.top,
      });

      const newNode: Node = {
        id: `${type}-${Date.now()}`,
        type: 'custom',
        position,
        data: { 
          type,
          label: nodeConfig.label,
          params: nodeConfig.params || {},
        },
      };

      setNodes((nds) => nds.concat(newNode));
    },
    [reactFlowInstance, setNodes]
  );

  const handleExecute = async () => {
    setIsLoading(true);
    setError(null);
    try {
      const backendGraphSpec = GraphTransformer.toBackendFormat(nodes, edges);
      const result = await executeGraph(backendGraphSpec);
      console.log('Graph execution result:', result);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
      console.error('Error executing graph:', err);
    } finally {
      setIsLoading(false);
    }
  };

  const handleImport = useCallback((event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onload = (e) => {
      try {
        const content = e.target?.result as string;
        const importedData = JSON.parse(content);
        let graphSpec, positions;
        if (importedData.nodes && importedData.edges) {
          graphSpec = importedData;
          positions = importedData.positions;
        } else {
          throw new Error('Invalid graph format');
        }
        const { nodes: importedNodes, edges: importedEdges } =
          GraphTransformer.fromBackendFormat(graphSpec, positions);
        setNodes(importedNodes);
        setEdges(importedEdges);
        setError(null);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to import graph');
        console.error('Error importing graph:', err);
      }
    };
    reader.readAsText(file);
  }, [setNodes, setEdges]);

  return (
    <div className="graph-container" ref={reactFlowWrapper}>
      <ReactFlow
        nodes={nodes}
        edges={edges}
        onNodesChange={onNodesChange}
        onEdgesChange={onEdgesChange}
        onConnect={onConnect}
        onInit={setReactFlowInstance}
        onDrop={onDrop}
        onDragOver={onDragOver}
        nodeTypes={nodeTypes}
        fitView
      >
        <Background />
        <Controls />
        <MiniMap />
        <Panel position="top-right">
          <div style={{ display: 'flex', gap: '8px' }}>
            <input
              type="file"
              accept=".json"
              onChange={handleImport}
              style={{ display: 'none' }}
              id="import-graph"
            />
            <label htmlFor="import-graph" style={{ cursor: 'pointer' }}>
              <button>Import Graph</button>
            </label>
            <button onClick={handleExecute} disabled={isLoading}>
              {isLoading ? 'Executing...' : 'Execute Graph'}
            </button>
          </div>
        </Panel>
      </ReactFlow>
      {error && <div className="error-message">{error}</div>}
    </div>
  );
} 