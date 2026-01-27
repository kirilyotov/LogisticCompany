import logging
from fastapi import FastAPI
from src.api.v1.routers import api_router
from src.core.exception_handlers import ExceptionHandlers

# Configure logging
logging.basicConfig(level=logging.INFO)

app = FastAPI()

# Register Exception Handlers
ExceptionHandlers.register(app)
app.include_router(api_router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"message": "Hello World"}
