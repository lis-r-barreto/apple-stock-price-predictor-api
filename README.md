# Apple Stock Price Prediction API

This project provides a FastAPI-based application to predict Apple stock prices for the next 30 days using a pre-trained LSTM model.

---

## **Setup Options**

### **1. Local Execution with Python (venv)**

#### **Steps**
1. **Set up a Virtual Environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Linux/Mac
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

2. **Run the Application**:
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

3. **Test the API**:
   - **Health Check**:
     ```bash
     curl http://localhost:8000/
     ```
   - **Make Predictions**:
     ```bash
     curl -X POST "http://localhost:8000/predict" \
       -H "Content-Type: application/json" \
       -d '{"csv_file_path": "data/apple_stock.csv"}'
     ```

4. **Deactivate the Virtual Environment**:
   ```bash
   deactivate
   ```

---

### **2. Docker Execution**

#### **Steps**
1. **Build the Docker Image**:
   ```bash
   docker build -t apple-stock-price-predictor-api .
   ```

2. **Run the Container**:
   ```bash
   docker run -p 8000:8000 apple-stock-price-predictor-api
   ```

3. **Test the API**:
   - **Health Check**:
     ```bash
     curl http://localhost:8000/
     ```
   - **Make Predictions**:
     ```bash
     curl -X POST "http://localhost:8000/predict" \
       -H "Content-Type: application/json" \
       -d '{"csv_file_path": "/data/apple_stock.csv"}'
     ```

4. **Stop and Remove the Container**:
   ```bash
   docker stop stock-prediction-api
   docker rm stock-prediction-api
   ```

---

## **Directory Structure**
```
project/
├── app/                 # Application code
│   ├── main.py          # FastAPI entry point
│   ├── routes/          # API routes
│   ├── utils/           # Utility modules
│   ├── model/           # Pre-trained model files
│   └── artifacts/       # Artifacts model files    
├── data/                # CSV data directory
├── requirements.txt     # Python dependencies
└── Dockerfile           # Docker configuration
```

---

## **Troubleshooting**

- **Missing Dependencies**:
  ```bash
  pip install -r requirements.txt
  ```

- **File Not Found Errors**:
  Ensure apple_stock.csv and model files exist in the correct paths.

- **Port Already in Use**:
  ```bash
  uvicorn app.main:app --reload --host 0.0.0.0 --port 8080
  ```

- **Check Docker Logs**:
  ```bash
  docker logs stock-prediction-api
  ```

---

---

## **API Details**

### **Endpoints**
- **Health Check**: `GET /`
  - Response: `{"status": "healthy"}`
- **Predictions**: `POST /predict`
  - Request Body:
    ```json
    {"csv_file_path": "data/apple_stock.csv"}
    ```
  - Response:
    ```json
    {
      "predictions": [
        {"date": "2025-05-23", "predicted_price": 198.45},
        {"date": "2025-05-24", "predicted_price": 199.12}
      ]
    }
    ```
- **Metrics**: `GET /metrics`
  - Response: Metrics in Prometheus format.
  - Example:
    ```
    # HELP request_count Total number of requests received
    # TYPE request_count counter
    request_count{method="GET",endpoint="/metrics"} 5
    # HELP request_latency_seconds Response time per endpoint
    # TYPE request_latency_seconds histogram
    request_latency_seconds_bucket{method="GET",endpoint="/metrics",le="0.005"} 3
    request_latency_seconds_sum{method="GET",endpoint="/metrics"} 0.012
    request_latency_seconds_count{method="GET",endpoint="/metrics"} 5
    ```

---

### **Test the Metrics Endpoint**
You can test the `/metrics` endpoint using `curl`:
```bash
curl http://localhost:8000/metrics
```

If Prometheus is configured correctly, it will scrape this endpoint and display the metrics in its dashboard.