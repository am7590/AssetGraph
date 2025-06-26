import React, { useState } from 'react';
import styled from '@emotion/styled';

const Container = styled.div`
  width: 100vw;
  height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background: #f8f9fa;
  gap: 2rem;
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
`;

const Title = styled.h1`
  color: #2c3e50;
  font-size: 2.5rem;
  margin-bottom: 2rem;
  text-align: center;
`;

const OptionsContainer = styled.div`
  display: flex;
  gap: 2rem;
  justify-content: center;
  width: 100%;
  max-width: 800px;
  padding: 0 1rem;
`;

const OptionCard = styled.div`
  background: white;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  width: 300px;
  cursor: pointer;
  transition: all 0.2s ease;
  text-align: center;

  &:hover {
    transform: translateY(-5px);
    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
  }
`;

const OptionTitle = styled.h2`
  color: #2c3e50;
  margin: 0 0 1rem 0;
  font-size: 1.5rem;
`;

const OptionDescription = styled.p`
  color: #666;
  margin: 0;
  line-height: 1.5;
  font-size: 1rem;
`;

const JsonInput = styled.textarea`
  width: 100%;
  max-width: 600px;
  height: 200px;
  padding: 1rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-family: monospace;
  margin-bottom: 1rem;
  resize: vertical;
`;

const Button = styled.button`
  padding: 0.75rem 1.5rem;
  background: #3498db;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: 500;
  width: 100%;
  max-width: 600px;
  font-size: 1rem;
  
  &:hover {
    background: #2980b9;
  }
`;

const ErrorMessage = styled.div`
  color: #e74c3c;
  margin-top: 1rem;
  text-align: center;
  max-width: 600px;
`;

interface LandingPageProps {
  onJsonSubmit: (json: any) => void;
  onCreateNew: () => void;
}

export const LandingPage: React.FC<LandingPageProps> = ({ onJsonSubmit, onCreateNew }) => {
  const [showJsonInput, setShowJsonInput] = useState(false);
  const [jsonInput, setJsonInput] = useState('');
  const [error, setError] = useState<string | null>(null);

  const handleJsonSubmit = () => {
    try {
      const parsedJson = JSON.parse(jsonInput);
      setError(null);
      onJsonSubmit(parsedJson);
    } catch (e) {
      setError('Invalid JSON format. Please check your input.');
    }
  };

  if (showJsonInput) {
    return (
      <Container>
        <Title>Import Graph</Title>
        <JsonInput
          value={jsonInput}
          onChange={(e) => setJsonInput(e.target.value)}
          placeholder="Paste your graph JSON here..."
        />
        <Button onClick={handleJsonSubmit}>Import Graph</Button>
        <Button onClick={() => setShowJsonInput(false)} style={{ background: '#95a5a6', marginTop: '0.5rem' }}>
          Back
        </Button>
        {error && <ErrorMessage>{error}</ErrorMessage>}
      </Container>
    );
  }

  return (
    <Container>
      <Title>Asset Graph</Title>
      <OptionsContainer>
        <OptionCard onClick={() => setShowJsonInput(true)}>
          <OptionTitle>Import Graph</OptionTitle>
          <OptionDescription>
            Upload or paste an existing graph configuration in JSON format to continue working on it.
          </OptionDescription>
        </OptionCard>
        <OptionCard onClick={onCreateNew}>
          <OptionTitle>Create New</OptionTitle>
          <OptionDescription>
            Start with a blank canvas and build your graph from scratch using the available node types.
          </OptionDescription>
        </OptionCard>
      </OptionsContainer>
    </Container>
  );
}; 