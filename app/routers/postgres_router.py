import os
from fastapi import APIRouter, HTTPException
from app.db_upload.postgres_functions import PostgresFunctions

pg_config = {
    'user': os.getenv('POSTGRES_USER'),
    'password': os.getenv('POSTGRES_PASSWORD'),
    'host': os.getenv('POSTGRES_HOST'),
    'port': os.getenv('POSTGRES_PORT'),
    'dbname': os.getenv('POSTGRES_DB')
}

postgres_router = APIRouter()
postgres_functions = PostgresFunctions(**pg_config)
engine = postgres_functions.create_connection()

csv_file = 'data/businesses_postgres.csv'


@postgres_router.post("/upload_data")
async def upload_postgres_data():
    try:
        postgres_functions.upload_data(engine, 'business_table', csv_file)
        return {"message": "Data uploaded successfully to PostgreSQL"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@postgres_router.get("/get_business/{business_id}")
async def get_postgres_business(business_id: str):
    try:
        business_info = postgres_functions.get_businesses('business_table', business_id)
        return business_info
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
