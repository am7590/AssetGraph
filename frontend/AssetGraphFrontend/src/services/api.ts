import type { GraphSpec } from '@/types/graph';

const API_BASE_URL = 'http://localhost:8000';

// Transform the graph spec to match backend expectations
const transformGraphSpec = (spec: GraphSpec): any => {
  console.log('Transforming graph spec:', spec);
  const transformed = {
    ...spec,
    edges: spec.edges.map(edge => ({
      from_: edge.from_ || edge.from,
      to: edge.to
    }))
  };
  console.log('Transformed spec:', transformed);
  return transformed;
};

export async function executeGraph(graphSpec: GraphSpec): Promise<any> {
  console.log('Executing graph with spec:', graphSpec);
  
  // Transform edges to use from_ instead of from
  const transformedSpec = {
    ...graphSpec,
    edges: graphSpec.edges.map(edge => ({
      from_: edge.from_ || edge.from,
      to: edge.to
    }))
  };
  
  console.log('Transformed graph spec:', transformedSpec);
  
  try {
    const response = await fetch('http://localhost:8000/api/execute-graph', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
      },
      body: JSON.stringify(transformedSpec)
    });

    console.log('Response status:', response.status);
    console.log('Response headers:', response.headers);
    
    const data = await response.json();
    console.log('Response data:', data);

    // If we have data, return it even if status is 500
    if (data && Object.keys(data).length > 0) {
      return data;
    }

    if (!response.ok) {
      console.error('Error response text:', await response.text());
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return data;
  } catch (error) {
    console.error('Error in executeGraph:', error);
    console.error('Error details:', {
      message: error instanceof Error ? error.message : 'Unknown error',
      stack: error instanceof Error ? error.stack : undefined
    });
    throw error;
  }
} 