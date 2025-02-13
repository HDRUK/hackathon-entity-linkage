import json
from rapidfuzz import process

from .elastic import find_elastic_dataset_matches, find_elastic_tools_matches


class Database:
    def __init__(self):
        self.datasets = []
        self.publications = []
        self.tools = []
        with open("./data/datasets.json") as f:
            self.datasets = json.load(f)
        with open("./data/publications.json") as f:
            self.publications = json.load(f)
        with open("./data/tools.json") as f:
            self.tools = json.load(f)


database = Database()


def find_best_matches(candidates, threshold=80):
    titles = [x["metadata"]["summary"]["title"] for x in database.datasets]

    matches = {}
    for cand in candidates:
        match_title, score, index = process.extractOne(cand, titles)

        if score >= threshold:
            data = database.datasets[index]
            matches[cand] = {
                "id": data["id"],
                "title": data["metadata"]["summary"]["title"],
            }
        else:
            matches[cand] = None

    return matches

def find_elastic_matches(candidates):
    matches = {}
    for c in candidates:
        matches[c] = find_elastic_dataset_matches(c)
    return matches
    