from fastapi import APIRouter
from prometheus_client import generate_latest, Counter, Histogram
from starlette.responses import Response
from app.utils.logging_dd import setup_logger

router = APIRouter()

logger = setup_logger(name="MetricsRoute")

@router.get("/metrics", tags=["Metrics"])
async def metrics():
    return Response(content=generate_latest(), media_type="text/plain")