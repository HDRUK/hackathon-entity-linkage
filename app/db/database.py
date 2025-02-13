import json


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
