import React, { memo, useState } from 'react';
import { Handle, Position, NodeProps } from 'reactflow';
import styled from '@emotion/styled';

const NodeContainer = styled.div`
  padding: 10px;
  border-radius: 5px;
  background: white;
  border: 1px solid #ddd;
  min-width: 200px;
`;

const NodeHeader = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
  padding-bottom: 5px;
  border-bottom: 1px solid #eee;
`;

const NodeTitle = styled.div`
  font-weight: bold;
  color: #333;
`;

const NodeId = styled.div`
  font-size: 0.8em;
  color: #666;
  background: #f5f5f5;
  padding: 2px 6px;
  border-radius: 3px;
  margin-left: 8px;
`;

const NodeContent = styled.div`
  display: flex;
  flex-direction: column;
  gap: 8px;
`;

const ParamGroup = styled.div`
  display: flex;
  flex-direction: column;
  gap: 4px;
`;

const ParamLabel = styled.label`
  font-size: 0.9em;
  color: #555;
  display: flex;
  flex-direction: column;
  gap: 2px;
`;

const ParamDescription = styled.span`
  font-size: 0.8em;
  color: #888;
  font-style: italic;
`;

const ParamInput = styled.input`
  padding: 4px 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 0.9em;
  width: 100%;
  &:focus {
    outline: none;
    border-color: #2196f3;
    box-shadow: 0 0 0 2px rgba(33, 150, 243, 0.1);
  }
`;

const HandleContainer = styled.div`
  position: absolute;
  width: 100%;
  height: 100%;
  top: 0;
  left: 0;
  pointer-events: none;
`;

const InputHandleContainer = styled.div`
  position: absolute;
  left: -60px;
  top: 50%;
  transform: translateY(-50%);
  display: flex;
  align-items: center;
  gap: 8px;
`;

const OutputHandleContainer = styled.div`
  position: absolute;
  right: -60px;
  top: 50%;
  transform: translateY(-50%);
  display: flex;
  align-items: center;
  gap: 8px;
`;

const HandleLabel = styled.div`
  font-size: 0.8em;
  color: #666;
  white-space: nowrap;
`;

interface ParamConfig {
  type: string;
  default: any;
  field: string;
  description?: string;
}

const formatNodeId = (id: string) => {
  return id.split('-')[0];
};

const CustomNode = ({ data, id }: NodeProps) => {
  const [params, setParams] = useState(data.params || {});

  const handleParamChange = (paramName: string, value: string) => {
    const newParams = { ...params, [paramName]: value };
    setParams(newParams);
    data.params = newParams;
  };

  const renderParamInput = (paramName: string, paramConfig: ParamConfig) => {
    const value = params[paramName] ?? paramConfig.default;
    const description = paramConfig.description || getDefaultDescription(paramName, paramConfig);

    return (
      <ParamGroup key={paramName}>
        <ParamLabel>
          {paramConfig.field}
          <ParamDescription>{description}</ParamDescription>
        </ParamLabel>
        <ParamInput
          type={paramConfig.type === 'number' ? 'number' : 'text'}
          value={value}
          onChange={(e) => handleParamChange(paramName, e.target.value)}
          placeholder={paramConfig.default?.toString() || ''}
        />
      </ParamGroup>
    );
  };

  const getDefaultDescription = (paramName: string, config: ParamConfig): string => {
    const descriptions: Record<string, Record<string, string>> = {
      LoadTickerData: {
        ticker: 'The stock symbol to fetch data for (e.g., AAPL, MSFT)',
        start_date: 'Start date in YYYY-MM-DD format',
        end_date: 'End date in YYYY-MM-DD format'
      },
      CalculateMovingAverage: {
        window_size: 'Number of periods to calculate the moving average over',
        column: 'The price column to use (e.g., close, high, low)'
      },
      CalculateRSI: {
        period: 'Number of periods to calculate RSI over (typically 14)',
        column: 'The price column to use for RSI calculation'
      },
      CalculateMACD: {
        fast_period: 'Number of periods for the fast EMA (typically 12)',
        slow_period: 'Number of periods for the slow EMA (typically 26)',
        signal_period: 'Number of periods for the signal line (typically 9)',
        column: 'The price column to use for MACD calculation'
      },
      Load10K: {
        ticker: 'The stock symbol to fetch 10-K for',
        year: 'The year of the 10-K filing'
      },
      Summarize10K: {
        section: 'The section of the 10-K to summarize (e.g., MD&A, Risk Factors)',
        max_length: 'Maximum length of the summary in characters'
      },
      LoadIncomeStatement: {
        period: 'Time period for the statement (annual or quarterly)',
        limit: 'Number of periods to fetch'
      },
      LoadBalanceSheet: {
        period: 'Time period for the statement (annual or quarterly)',
        limit: 'Number of periods to fetch'
      },
      LoadCashFlow: {
        period: 'Time period for the statement (annual or quarterly)',
        limit: 'Number of periods to fetch'
      },
      GenerateLLMReport: {
        report_type: 'Type of report to generate (full, summary, or financial_analysis)'
      }
    };

    return descriptions[data.type]?.[paramName] || `Enter ${config.field.toLowerCase()}`;
  };

  return (
    <NodeContainer>
      <HandleContainer>
        <InputHandleContainer>
          <HandleLabel>Input</HandleLabel>
          <Handle type="target" position={Position.Left} style={{ background: '#2196f3' }} />
        </InputHandleContainer>
        <OutputHandleContainer>
          <Handle type="source" position={Position.Right} style={{ background: '#4CAF50' }} />
          <HandleLabel>Output</HandleLabel>
        </OutputHandleContainer>
      </HandleContainer>
      <NodeHeader>
        <NodeTitle>{data.label}</NodeTitle>
        <NodeId>{formatNodeId(id)}</NodeId>
      </NodeHeader>
      <NodeContent>
        {Object.entries(data.params || {}).map(([paramName, paramConfig]) =>
          renderParamInput(paramName, paramConfig as ParamConfig)
        )}
      </NodeContent>
    </NodeContainer>
  );
};

export default memo(CustomNode); 