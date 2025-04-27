from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from backend.models.graph_spec import GraphSpec
from backend.core.graph_runner import run_graph, GraphState
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/execute-graph", response_model=GraphState)
async def execute_graph(graph_spec: GraphSpec):
    logger.info(f"Received request to execute graph: {graph_spec.dict()}")
    try:
        result: GraphState = await run_graph(graph_spec)
        logger.info(f"Graph execution finished. Result errors: {result.get('errors')}")

        # Check if any errors were recorded in the state
        if result.get("errors"):
            # Return 500 Internal Server Error, but include the result payload
            # which now contains the error details.
            return JSONResponse(
                status_code=500,
                content=result
            )
        else:
            # Return 200 OK with the successful result
            return JSONResponse(
                status_code=200,
                content=result
            )

    except ValueError as ve:
        # Handle graph validation errors (e.g., unknown node type, no nodes)
        logger.error(f"Graph validation error: {ve}")
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        # Catch unexpected errors during graph execution setup or invocation
        logger.exception("Unexpected error during graph execution:") # Log full traceback
        raise HTTPException(status_code=500, detail=f"An unexpected server error occurred: {e}")
