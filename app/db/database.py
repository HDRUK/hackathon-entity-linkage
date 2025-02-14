import json
import os


class Database:
    def __init__(self):
        self.datasets = []
        self.publications = []
        self.tools = []
        self.linkages_file = "./data/found_linkages.json"

        with open("./data/datasets.json") as f:
            self.datasets = json.load(f)
        with open("./data/publications.json") as f:
            self.publications = json.load(f)
        with open("./data/tools.json") as f:
            self.tools = json.load(f)

        if not os.path.exists(self.linkages_file):
            with open(self.linkages_file, "w") as f:
                json.dump([], f)

    def save_linkages(self, data):
        if not data:
            return
        with open(self.linkages_file, "r") as f:
            linkages = json.load(f)

        linkages.append(data)

        with open(self.linkages_file, "w") as f:
            json.dump(linkages, f, indent=4)

    def get_linkages(self):
        """Retrieve all saved linkages from linkages.json."""
        with open(self.linkages_file, "r") as f:
            linkages = json.load(f)

        return linkages

    def delete_linkages(self):
        with open(self.linkages_file, "w") as f:
            json.dump([], f, indent=4)


database = Database()
