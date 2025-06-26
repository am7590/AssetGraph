import { BackendGraphSpec } from '../types/graph';
import { GraphValidator } from './graphValidator';

export const executeGraph = async (graphSpec: BackendGraphSpec): Promise<any> => {
  // Pre-execution validation
  const validation = GraphValidator.validateGraphSpec(graphSpec);
  if (!validation.isValid) {
    throw new Error(`Graph validation failed: ${validation.errors.join(', ')}`);
  }

  try {
    const response = await fetch('http://localhost:8000/api/execute-graph', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(graphSpec),
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || `HTTP ${response.status}: Failed to execute graph`);
    }

    return await response.json();
  } catch (error) {
    console.error('Error executing graph:', error);
    if (error instanceof TypeError && error.message.includes('fetch')) {
      throw new Error('Network error: Unable to connect to backend server');
    }
    throw error;
  }
}; 