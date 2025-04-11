import os
from fastapi import FastAPI, HTTPException
from tortoise.contrib.fastapi import register_tortoise
from dotenv import load_dotenv

from app.api.routes import router

# Load environment variables
load_dotenv()

# Create FastAPI app
app = FastAPI(
    title="Financial Data API",
    description="API for managing complex financial data structures with Tortoise ORM",
    version="1.0.0"
)

# Add API routes
app.include_router(router, prefix="/api")

# Register Tortoise ORM
DATABASE_URL = os.getenv("DATABASE_URL", "postgres://postgres:postgres@db:5432/financial_api")

TORTOISE_ORM = {
    "connections": {"default": DATABASE_URL},
    "apps": {
        "models": {
            "models": ["app.models.financial_data", "aerich.models"],
            "default_connection": "default",
        },
    },
    "use_tz": False,
    "timezone": "UTC"
}

register_tortoise(
    app,
    config=TORTOISE_ORM,
    generate_schemas=True,  # Generate schemas automatically for now
    add_exception_handlers=True,
)

@app.get("/")
async def root():
    return {"message": "Welcome to Financial Data API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
