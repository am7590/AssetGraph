# AssetGraph - Backend

## Prerequisites

- Python 3.9+
- An API key from [Financial Modeling Prep](https://site.financialmodelingprep.com/)

## Setup

1.  **Clone the repository**

2.  **Set up environment variables:**

    - Copy the example environment file:
      ```bash
      cp .env.example .env
      ```
    - Edit the `.env` file and add your FMP API key:
      ```
      FMP_API_KEY=YOUR_ACTUAL_FMP_API_KEY
      ```

3.  **Install Python dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

## Running the Server

From the project root directory (`AssetGraph`), run the FastAPI server using uvicorn:

```bash
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

The `--reload` flag automatically restarts the server when code changes are detected. The API will be available at `http://localhost:8000`.

## Testing the Endpoint

You can test the `/api/execute-graph` endpoint by sending a POST request with a `GraphSpec` JSON payload.

**Example using `curl`:**

```bash
curl -X POST http://localhost:8000/api/execute-graph \
-H "Content-Type: application/json" \
-d '{
  "nodes": [
    { "id": "load", "type": "LoadTickerData", "params": { "ticker": "AAPL" } },
    { "id": "preprocess", "type": "PreprocessFinancials", "params": {} },
    { "id": "summarize", "type": "SummarizeIncomeStatement", "params": {} },
    { "id": "report", "type": "GenerateMarkdownReport", "params": {} }
  ],
  "edges": [
    { "from_": "load", "to": "preprocess" },
    { "from_": "preprocess", "to": "summarize" },
    { "from_": "summarize", "to": "report" }
  ]
}'
```
