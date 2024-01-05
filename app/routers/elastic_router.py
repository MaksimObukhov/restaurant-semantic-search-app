from fastapi import APIRouter, HTTPException
from app.db_upload.elastic_functions import ElasticFunctions

elastic_router = APIRouter()
elastic_functions = ElasticFunctions(index_name='restaurant_search')

# csv_file = 'data/reviews_elastic_sample.csv'
csv_file = 'data/embeddings_businesses_df.csv'


@elastic_router.post("/upload_data")
async def upload_elastic_data():
    try:
        elastic_functions.create_index()
        elastic_functions.upload_data(csv_file)
        return {"message": "Data uploaded successfully to Elasticsearch"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@elastic_router.get("/search_elastic/{query}")
async def search_elastic_businesses(query: str):
    try:
        results = elastic_functions.search_businesses(query)
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
