# Importing necessary libraries
import pandas as pd
from elasticsearch import Elasticsearch

def elastic_search_init():
    # Load the embedded data
    data = pd.read_csv('../data/investment_data.csv')
    records = data.to_dict(orient='records')

    # Initialize the client 
    es_client = Elasticsearch('http://localhost:9200')

    # Create the Schema of the Elastic Search Index for vector search
    index_settings = {
        "settings": {
            "number_of_shards": 1,
            "number_of_replicas": 0
        },
        "mappings": {
            "properties": {
                "question": {"type": "text"},
                "answer": {"type": "text"},
                "context": {"type": "text"},
                "ticker": {"type": "keyword"}, 
                "company": {"type": "keyword"},
                "id": {"type": "keyword"},
                "question_answer_context_vector": {
                    "type": "dense_vector",
                    "dims": 384,             
                    "index": True,
                    "similarity": "cosine"
                }
            }
        }
    }

    # Provide the name of the index
    index_name = "investment-info"
    # Check if the index exists
    if es_client.indices.exists(index=index_name):
        # Delete the existing index
        es_client.indices.delete(index=index_name)
    # Create the elastic search index
    response = es_client.indices.create(index=index_name, body=index_settings)
    # Verify that elastic search is created
    print(response)

    # Fetch all the documents into the elastic search index
    for record in records:
        es_client.index(index = index_name, document=record)

if __name__ == "__main__":
    print("Setting up elastic search database")
    elastic_search_init()
    print("Elastic search database")
