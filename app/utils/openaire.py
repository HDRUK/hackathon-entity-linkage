import requests
import json


openaire_search_base = "https://api.openaire.eu/search"
openaire_graph_base = "https://api.openaire.eu/graph"

def openaire_search(title, entity_type="datasets"):
    '''
    title: string - title of the entity we are seraching for'
    '''
    search_url = "%s/%s?title=%s&format=json" % (openaire_search_base, entity_type, title)
    response = requests.get(search_url)
    response_dict = response.json()
    result_ids = []
    for hit in response_dict["response"]["results"]["result"]:
        result_ids.append(hit["header"]["dri:objIdentifier"]["$"])
    return result_ids

def openaire_graph(result_ids, entity_type="researchProducts"):
    '''
    retrieve all info about the given id
    '''
    dataset_titles = []
    for id in result_ids:
        graph_url = "%s/%s/%s" % (openaire_graph_base, entity_type, id)
        response = requests.get(graph_url)
        dataset_titles.append(response.json()["mainTitle"])
    return dataset_titles


