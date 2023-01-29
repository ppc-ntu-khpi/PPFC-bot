import json

class Subject:
    def __init__(self, jsonDict):
        self.id = jsonDict["id"]
        self.name = jsonDict["name"]
