from fastapi import FastAPI
from app.routers.elastic_router import elastic_router
from app.routers.postgres_router import postgres_router

app = FastAPI()

# Include routers
app.include_router(elastic_router, prefix="/elastic", tags=["elastic"])
app.include_router(postgres_router, prefix="/postgres", tags=["postgres"])
