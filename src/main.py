from fastapi import FastAPI

from src.versions.api.routes import index as apiRoutes

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello world!"}

app.include_router(apiRoutes.router, prefix="/api")