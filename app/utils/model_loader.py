import os
from tensorflow.keras.models import load_model
from tensorflow.keras.losses import MeanSquaredError
from app.utils.logging_dd import setup_logger

logger = setup_logger(name="ModelLoader")

def load_lstm_model():
    """
    Loads the trained LSTM model.

    Returns:
        keras.Model: The loaded LSTM model.

    Raises:
        FileNotFoundError: If the model file is not found.
    """
    model_path = "model/lstm_apple_stock.h5"
    logger.info("Starting LSTM model loading.")

    # Check if the model file exists
    if not os.path.exists(model_path):
        logger.error(f"Model file not found: {model_path}")
        raise FileNotFoundError(f"Model file not found: {model_path}")

    logger.info(f"Model file found: {model_path}. Loading the model...")
    try:
        model = load_model(model_path, custom_objects={"mse": MeanSquaredError()})
        logger.info("LSTM model loaded successfully.")
        return model
    except Exception as e:
        logger.error(f"Error loading the LSTM model: {e}")
        raise
