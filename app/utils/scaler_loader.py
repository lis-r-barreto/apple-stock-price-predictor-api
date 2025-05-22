import os
import joblib
from app.utils.logging_dd import setup_logger

logger = setup_logger(name="ScalerLoader")

def load_scaler():
    scaler_path = "artifacts/min_max_scaler.joblib"
    logger.info("Starting scaler loading.")

    if not os.path.exists(scaler_path):
        logger.error(f"Scaler file not found: {scaler_path}")
        raise FileNotFoundError(f"Scaler file not found: {scaler_path}")

    logger.info(f"Scaler file found: {scaler_path}. Loading the scaler...")
    try:
        scaler = joblib.load(scaler_path)
        logger.info("Scaler loaded successfully.")
        return scaler
    except Exception as e:
        logger.error(f"Error loading the scaler: {e}")
        raise
