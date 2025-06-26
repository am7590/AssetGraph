import React from 'react';
import styled from '@emotion/styled';
import { Node, Edge } from 'reactflow';

const SidebarContainer = styled.div`
  width: 250px;
  height: 100%;
  background: white;
  border-right: 1px solid #ddd;
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 20px;
`;

const Title = styled.h2`
  margin: 0;
  color: #2c3e50;
  font-size: 1.2em;
`;

const NodeTypesContainer = styled.div`
  display: flex;
  flex-direction: column;
  gap: 10px;
`;

const NodeType = styled.div`
  padding: 10px;
  background: #f8f9fa;
  border: 1px solid #ddd;
  border-radius: 4px;
  cursor: grab;
  user-select: none;
  transition: all 0.2s ease;

  &:hover {
    background: #e9ecef;
    transform: translateY(-2px);
  }

  &:active {
    cursor: grabbing;
  }
`;

const Button = styled.button`
  padding: 10px 20px;
  background: #3498db;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: 500;
  margin-top: auto;
  
  &:hover {
    background: #2980b9;
  }
`;

interface SidebarProps {
  onGenerateJson: (nodes: Node[], edges: Edge[]) => void;
}

const nodeTypes = [
  { type: 'LoadTickerData', label: 'Load Ticker Data' },
  { type: 'LoadIncomeStatement', label: 'Load Income Statement' },
  { type: 'LoadBalanceSheet', label: 'Load Balance Sheet' },
  { type: 'LoadCashFlow', label: 'Load Cash Flow' },
  { type: 'PreprocessFinancials', label: 'Preprocess Financials' },
  { type: 'SummarizeIncomeStatement', label: 'Summarize Income Statement' },
  { type: 'GenerateLLMReport', label: 'Generate LLM Report' },
];

export const Sidebar: React.FC<SidebarProps> = ({ onGenerateJson }) => {
  const onDragStart = (event: React.DragEvent, nodeType: string) => {
    event.dataTransfer.setData('application/reactflow', nodeType);
    event.dataTransfer.effectAllowed = 'move';
  };

  return (
    <SidebarContainer>
      <Title>Node Types</Title>
      <NodeTypesContainer>
        {nodeTypes.map((node) => (
          <NodeType
            key={node.type}
            draggable
            onDragStart={(e) => onDragStart(e, node.type)}
          >
            {node.label}
          </NodeType>
        ))}
      </NodeTypesContainer>
      <Button onClick={() => onGenerateJson([], [])}>
        Generate JSON
      </Button>
    </SidebarContainer>
  );
}; 