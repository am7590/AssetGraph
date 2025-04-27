import logging
from fastapi import FastAPI
from backend.api.routes import submit_graph

# Basic logging configuration
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = FastAPI(title="FinRobot 2.0 Backend")

logger.info("Including /api router")
app.include_router(submit_graph.router, prefix="/api")

@app.get("/")
def read_root():
    logger.info("Root endpoint requested")
    return {"message": "FinRobot 2.0 backend running"}

logger.info("FastAPI app configured.")
