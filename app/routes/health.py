from fastapi import APIRouter
from app.utils.logging_dd import setup_logger

logger = setup_logger(name="HealthRoute")

router = APIRouter()

@router.get("/")
def api_health():
    """
    Endpoint to check the API health.
    """
    logger.info("Health check endpoint accessed.")
    return {"status": "healthy"}
