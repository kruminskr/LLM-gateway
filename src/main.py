from fastapi import FastAPI

from src.versions.api.routes import gateway_routes
from src.versions.api.routes import health_routes

app = FastAPI()

# health check routes
app.include_router(health_routes.router, prefix="/api")

# gateway routes
app.include_router(gateway_routes.router, prefix="/api/gateway")