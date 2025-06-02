import os
import numpy as np
import pandas as pd
from utils.model_loader import load_lstm_model
from utils.scaler_loader import load_scaler
from utils.logging_dd import setup_logger

logger = setup_logger(name="PredictionLogic")


def validate_csv_file(csv_file_path: str):
    if not os.path.exists(csv_file_path):
        logger.error(f"CSV file not found: {csv_file_path}")
        raise FileNotFoundError(f"File not found: {csv_file_path}")
    logger.info(f"CSV file found: {csv_file_path}")


def load_and_validate_data(csv_file_path: str):
    data = pd.read_csv(csv_file_path)
    required_columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume']
    if not all(column in data.columns for column in required_columns):
        logger.error("Required columns are missing in the CSV file.")
        raise ValueError(f"CSV file must contain the following columns: {', '.join(required_columns)}")
    logger.info(f"CSV data successfully loaded. Total rows: {len(data)}")
    return data


def prepare_data_for_model(data: pd.DataFrame):
    features = data[['Open', 'High', 'Low', 'Close', 'Volume']].values
    sequence_length = 60
    if len(features) < sequence_length:
        logger.error("Insufficient data to create the input sequence.")
        raise ValueError("Insufficient data for prediction. At least 60 rows are required.")
    last_sequence = features[-sequence_length:]
    input_data = np.expand_dims(last_sequence, axis=0)
    logger.info("Data successfully prepared for the model.")
    return input_data


def generate_predictions(model, scaler, input_data, future_dates):
    predicted_prices_actual = []
    for future_date in future_dates:
        logger.debug(f"Generating prediction for date: {future_date.strftime('%Y-%m-%d')}")
        predicted_price_scaled = model.predict(input_data)[0, 0]
        num_features = scaler.n_features_in_
        dummy_predictions = np.zeros((1, num_features))
        dummy_predictions[:, 3] = predicted_price_scaled
        predicted_price_actual = scaler.inverse_transform(dummy_predictions)[:, 3][0]
        predicted_prices_actual.append(predicted_price_actual)
        logger.debug(f"Predicted price for {future_date.strftime('%Y-%m-%d')}: {predicted_price_actual:.2f}")
        next_input = np.append(input_data[0, 1:], [[predicted_price_actual] * 5], axis=0)
        input_data = np.expand_dims(next_input, axis=0)
    return predicted_prices_actual


def predict_prices(csv_file_path: str):
    logger.info("Starting price prediction.")
    validate_csv_file(csv_file_path)
    data = load_and_validate_data(csv_file_path)
    input_data = prepare_data_for_model(data)
    model = load_lstm_model()
    scaler = load_scaler()
    last_date = pd.to_datetime(data['Date'].iloc[-1])
    future_dates = [last_date + pd.Timedelta(days=i) for i in range(1, 31)]
    predicted_prices_actual = generate_predictions(model, scaler, input_data, future_dates)
    logger.info("Predictions successfully completed.")
    return [
        {"date": date.strftime('%Y-%m-%d'), "predicted_price": price}
        for date, price in zip(future_dates, predicted_prices_actual)
    ]
