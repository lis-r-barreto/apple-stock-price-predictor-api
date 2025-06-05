from fastapi import FastAPI, Request
from app.routes.health import router as health_router
from app.routes.prediction import router as prediction_router
from app.routes.metrics import router as metrics_router
from prometheus_client import Counter, Histogram

app = FastAPI(
    title="Stock Prediction API",
    openapi_tags=[
        {"name": "Health", "description": "Get API health"},
        {"name": "Prediction", "description": "Stock price prediction"},
        {"name": "Metrics", "description": "API metrics"},
    ],
)

REQUEST_COUNT = Counter("request_count", "Total number of requests received", ["method", "endpoint"])
REQUEST_LATENCY = Histogram("request_latency_seconds", "Response time per endpoint", ["method", "endpoint"])

@app.middleware("http")
async def prometheus_middleware(request: Request, call_next):
    method = request.method
    endpoint = request.url.path
    REQUEST_COUNT.labels(method=method, endpoint=endpoint).inc()
    response = None
    try:
        with REQUEST_LATENCY.labels(method=method, endpoint=endpoint).time():
            response = await call_next(request)
    except Exception as e:
        raise e
    return response


app.include_router(metrics_router)
app.include_router(health_router)
app.include_router(prediction_router)
