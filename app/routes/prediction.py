from fastapi import APIRouter, HTTPException
from app.schemas.stock_request import StockDataRequest
from app.utils.prediction_logic import predict_prices
from app.utils.logging_dd import setup_logger

logger = setup_logger(name="PredictionRoute")

router = APIRouter()

@router.post("/predict")
def predict(request: StockDataRequest):
    """
    Endpoint to predict stock prices for the next 30 days.
    """
    logger.info("Received request for stock price prediction.")
    logger.debug(f"Request payload: {request}")

    try:
        predictions = predict_prices(request.csv_file_path)
        logger.info("Stock price prediction completed successfully.")
        return {"predictions": predictions}
    except FileNotFoundError as e:
        logger.error(f"File not found error: {e}")
        raise HTTPException(status_code=404, detail=str(e))
    except ValueError as e:
        logger.error(f"Validation error: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
