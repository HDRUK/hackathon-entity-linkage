import requests
import json
import os
from elasticsearch import Elasticsearch
from dotenv import load_dotenv

load_dotenv()

ELASTIC_SERVICE_URL=os.environ.get("ELASTIC_SERVICE_URL")
ELASTICSEARCH_USER=os.environ.get("ELASTICSEARCH_USER")
ELASTICSEARCH_PASS=os.environ.get("ELASTICSEARCH_PASS")

client = Elasticsearch(
    ELASTIC_SERVICE_URL,
    basic_auth=(ELASTICSEARCH_USER, ELASTICSEARCH_PASS),
    verify_certs=False
)

def find_elastic_dataset_matches(title):
    payload = {
        "match": {
            "shortTitle": {
                "query": title
            }
        }
    }
    response = client.search(index="dataset", query=payload)
    matched_datasets = []
    for dataset in response["hits"]["hits"]:
        matched_datasets.append({
            "id": dataset["_id"], 
            "shortTitle": dataset["_source"]["shortTitle"],
            "score": dataset["_score"]
        })
    
    if len(matched_datasets) > 0:
        return matched_datasets
    else:
        return None

def find_elastic_tools_matches(name):
    payload = {
        "match": {
            "name": {
                "query": name
            }
        }
    }
    response = client.search(index="tool", query=payload)
    matched_tools = []
    for tool in response["hits"]["hits"]:
        matched_tools.append({
            "id": tool["_id"], 
            "name": tool["_source"]["name"],
            "score": dataset["_score"]
        })
    
    if len(matched_tools) > 0:
        return matched_tools
    else:
        return None