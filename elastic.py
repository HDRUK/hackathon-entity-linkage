import requests
import json
from dotenv import load_dotenv
import os
from elasticsearch import Elasticsearch

load_dotenv()

ELASTIC_SERVICE_URL=os.getenv("ELASTIC_SERVICE_URL")
ELASTICSEARCH_USER=os.getenv("ELASTICSEARCH_USER")
ELASTICSEARCH_PASS=os.getenv("ELASTICSEARCH_PASS")
ELASTICSEARCH_VERIFY_SSL=os.getenv("ELASTICSEARCH_VERIFY_SSL")

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
        matched_datasets.append({"id": dataset["_id"], "name": dataset["_source"]["name"]})
    return matched_datasets

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
        matched_tools.append({"id": tool["_id"], "name": tool["_source"]["name"]})
    return matched_tools