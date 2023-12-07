from elasticsearch import Elasticsearch
from sentence_transformers import SentenceTransformer
import os
import numpy as np


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


helper_token = Tokenizer(model_name='all-mpnet-base-v2')
# TODO: set input
INPUT = "ice cream cafe"
token_vector = helper_token.get_token(str(INPUT))

query = {
    "field": "np_embeddings",
    "query_vector": token_vector,
    "k": 10,
    "num_candidates": 50
}

es = Elasticsearch([{'scheme': 'http', 'host': 'localhost', 'port': 9200}])
res = es.search(index='restaurant_reviews',
                knn=query,
                request_timeout=55)
# TODO: find a way to transport results into postgres
ids = [x['_source']['business_id'] for x in res['hits']['hits']]
print(ids)
