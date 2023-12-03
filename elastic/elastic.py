from fastapi import FastAPI, HTTPException
from elasticsearch import Elasticsearch
from sentence_transformers import SentenceTransformer
from ast import literal_eval
import pandas as pd
import numpy as np
import psycopg2
from psycopg2 import extras
import os

app = FastAPI()
es = Elasticsearch([{'scheme': 'http', 'host': 'elasticsearch', 'port': 9200}])

pg_config = {
    'user': os.getenv('POSTGRES_USER'),
    'password': os.getenv('POSTGRES_PASSWORD'),
    'host': os.getenv('POSTGRES_HOST'),
    'port': os.getenv('POSTGRES_PORT'),
    'dbname': os.getenv('POSTGRES_DB')
}


df = pd.read_csv('data/reviews_elastic_sample.csv')
df['np_embeddings'] = df['np_embeddings'].apply(literal_eval)


@app.get("/")
async def root():
    return {"message": "Welcome to the Restaurant Search API!"}


class Tokenizer(object):
    def __init__(self, model_name):
        self.model_name = model_name
        self.model = SentenceTransformer(model_name)

    def get_token(self, documents):
        sentences = [documents]
        sentence_embeddings = self.model.encode(sentences)
        _ = list(sentence_embeddings.flatten())
        encod_np_array = np.array(_)
        encod_list = encod_np_array.tolist()
        return encod_list


index_name = 'restaurant_search'

# Create the index (if not exists)
if not es.indices.exists(index=index_name):
    es.indices.create(index=index_name)


def upload_data_to_elasticsearch(data):
    for record in data.to_dict("records"):
        try:
            es.index(index=index_name, body=record)
        except Exception as e:
            raise e


@app.post("/upload_data")
async def upload_data():
    try:
        upload_data_to_elasticsearch(df)
        return {"message": "Data uploaded successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/{business_id}")
async def get_business(business_id: str):
    try:
        result = es.search(index=index_name, body={"query": {"match": {"business_id": business_id}}})
        return result["hits"]["hits"]

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Function to query PostgreSQL
def get_restaurant_info_from_pg(business_id: str):
    try:
        conn = psycopg2.connect(**pg_config)
        cursor = conn.cursor(cursor_factory=extras.RealDictCursor)

        query = "SELECT * FROM business_table WHERE business_id = %s"
        cursor.execute(query, (business_id,))
        restaurant_info = cursor.fetchone()

        cursor.close()
        conn.close()

        return restaurant_info

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error querying PostgreSQL: {str(e)}")


helper_token = Tokenizer(model_name='all-mpnet-base-v2')


@app.get("/search/{query}")
async def search_businesses(query: str):
    try:
        # Get token vector for the input query
        token_vector = helper_token.get_token(query)

        # Define the KNN query
        knn_query = {
            "field": "np_embeddings",
            "query_vector": token_vector,
            "k": 10,
            "num_candidates": 50
        }

        # Perform KNN search
        result = es.search(index=index_name, knn=knn_query, request_timeout=55)

        # Extract relevant information from the result
        results_dict = [{'business_id': hit['_source']['business_id'],
                         'score': hit['_score']}
                        for hit in result['hits']['hits']]

        for business in results_dict:
            business['restaurant_info'] = get_restaurant_info_from_pg(business['business_id'])
        return results_dict

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
async def health_check():
    return {"status": "OK"}
