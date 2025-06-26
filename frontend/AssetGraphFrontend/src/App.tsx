import React, { useState, useRef } from 'react';
import './App.css';
import { Graph } from './components/Graph';
import { Sidebar } from './components/Sidebar';
import { LandingPage } from './components/LandingPage';
import { Node, Edge } from 'reactflow';
import { GraphTransformer } from './services/graphTransformer';

function App() {
  const [showGraph, setShowGraph] = useState(false);
  const [jsonData, setJsonData] = useState<any>(null);
  const [showJsonPreview, setShowJsonPreview] = useState(false);
  const [initialNodes, setInitialNodes] = useState<Node[]>([]);
  const [initialEdges, setInitialEdges] = useState<Edge[]>([]);
  const nodesRef = useRef<Node[]>([]);
  const edgesRef = useRef<Edge[]>([]);

  const handleJsonSubmit = (json: any) => {
    try {
      // Validate the imported data
      if (!json.nodes || !Array.isArray(json.nodes) || !json.edges || !Array.isArray(json.edges)) {
        throw new Error('Invalid graph format: missing nodes or edges arrays');
      }

      // Convert the imported data to React Flow format
      const nodes = json.nodes.map((node: any) => ({
        id: node.id,
        type: 'custom',
        position: node.position || { x: 0, y: 0 },
        data: {
          type: node.type,
          label: node.label || node.type,
          params: node.params || {},
        },
      }));

      const edges = json.edges.map((edge: any) => ({
        id: `${edge.from_ || edge.source}-${edge.to || edge.target}`,
        source: edge.from_ || edge.source,
        target: edge.to || edge.target,
        type: 'smoothstep',
        animated: true,
      }));

      setInitialNodes(nodes);
      setInitialEdges(edges);
      setJsonData(json);
      setShowGraph(true);
    } catch (error) {
      console.error('Error importing graph:', error);
      alert(error instanceof Error ? error.message : 'Failed to import graph');
    }
  };

  const handleCreateNew = () => {
    setJsonData(null);
    setInitialNodes([]);
    setInitialEdges([]);
    setShowGraph(true);
  };

  const handleGenerateJson = (nodes: Node[], edges: Edge[]) => {
    nodesRef.current = nodes;
    edgesRef.current = edges;
  };

  const handleShowJson = () => {
    const backendGraphSpec = GraphTransformer.toBackendFormat(nodesRef.current, edgesRef.current);
    setJsonData(backendGraphSpec);
    setShowJsonPreview(true);
  };

  const handleCopyJson = () => {
    if (jsonData) {
      navigator.clipboard.writeText(JSON.stringify(jsonData));
    }
  };

  if (!showGraph) {
    return <LandingPage onJsonSubmit={handleJsonSubmit} onCreateNew={handleCreateNew} />;
  }

  return (
    <div className="app">
      <div className="main-content">
        <Graph 
          onGenerateJson={handleGenerateJson} 
          initialNodes={initialNodes}
          initialEdges={initialEdges}
        />
        <Sidebar onGenerateJson={handleShowJson} />
      </div>
      {showJsonPreview && jsonData && (
        <div className="json-preview">
          <div className="json-preview-content">
            <button className="close-button" onClick={() => setShowJsonPreview(false)}>×</button>
            <button className="copy-button" onClick={handleCopyJson}>Copy</button>
            <pre>{JSON.stringify(jsonData)}</pre>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;
