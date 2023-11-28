# попробовать сделать поиск через reviews_elastic.csv, где: id, np_embeddings
# или попробовать побъеденить все отзывы в нестед джсон и закинуть в эластик, чтобы искал по одному большому полю

from elasticsearch import Elasticsearch
import pandas as pd
import os
from ast import literal_eval

# TODO: change path for docker
os.chdir("/Users/maksim/Documents/VSE/5. Semester/Text Analytics 2/semantic_search_restaurant")

# Read your CSV file into a Pandas DataFrame
df = pd.read_csv('data/reviews_elastic.csv').sample(1000, random_state=42, ignore_index=True)
df['np_embeddings'] = df['np_embeddings'].apply(literal_eval)

# Initialize Elasticsearch client
es = Elasticsearch([{'scheme': 'http', 'host': 'localhost', 'port': 9200}])

# Define the index name
index_name = 'restaurant_reviews'

# Delete the index if it already exists (optional)
if es.indices.exists(index=index_name):
    es.indices.delete(index=index_name)

# Create the index with a dense_vector field mapping
es.indices.create(
    index=index_name,
    body={
        "mappings": {
            "properties": {
                "business_id": {"type": "keyword"},
                "np_embeddings": {"type": "dense_vector", "dims": len(df['np_embeddings'][0])}
            }
        }
    }
)

elk_data = df.to_dict("records")

for record in elk_data:
    try:
        es.index(index=index_name, body=record)
    except Exception as e:
        raise
