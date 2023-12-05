from ast import literal_eval
import pandas as pd
from elasticsearch import Elasticsearch
from sentence_transformers import SentenceTransformer


class ElasticFunctions:
    def __init__(self, index_name):
        self.es = Elasticsearch([{'scheme': 'http', 'host': 'elasticsearch', 'port': 9200}])
        self.index_name = index_name
        self.model = SentenceTransformer('all-mpnet-base-v2')

    def create_index(self):
        if not self.es.indices.exists(index=self.index_name):
            self.es.indices.create(index=self.index_name)

    def upload_data(self, csv_file):
        data = pd.read_csv(csv_file)
        data['np_embeddings'] = data['np_embeddings'].apply(literal_eval)
        for record in data.to_dict("records"):
            try:
                self.es.index(index=self.index_name, body=record)
            except Exception as e:
                raise e

    def search_businesses(self, query):
        token_vector = self.get_token(query)

        knn_query = {
            "field": "np_embeddings",
            "query_vector": token_vector,
            "k": 10,
            "num_candidates": 50
        }

        result = self.es.search(index=self.index_name, knn=knn_query, request_timeout=55)

        results_dict = [{'business_id': hit['_source']['business_id'], 'score': hit['_score']}
                        for hit in result['hits']['hits']]

        return results_dict

    def get_token(self, documents):
        sentences = [documents]
        sentence_embeddings = self.model.encode(sentences)
        encod_list = sentence_embeddings.flatten().tolist()
        return encod_list
