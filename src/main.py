# src/main.py
from fastapi import FastAPI
from src.modules.auth.router import router as auth_router
from src.modules.customers.router import router as customer_router

app = FastAPI(title="Modular Monolith API", version="1.0.0")

app.include_router(auth_router, prefix="/api/v1/auth", tags=["Auth"])
app.include_router(customer_router, prefix="/api/v1/customers", tags=["Customers"])


@app.get("/health")
def health_check():
    return {"status": "healthy"}
