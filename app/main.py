from fastapi import FastAPI
from routes import prediction, health

# Inicializa a aplicação FastAPI
app = FastAPI(
    title="Stock Prediction API",
    openapi_tags=[
        {"name": "Health", "description": "Get API health"},
        {"name": "Prediction", "description": "Stock price prediction"},
    ],
)

# Inclui as rotas
app.include_router(health.router, tags=["Health"])
app.include_router(prediction.router, tags=["Prediction"])
