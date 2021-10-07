import json

class Relation:
    def __init__(self,json_data):
        self.raw_object = json.loads(json_data)
        self.bot_name = self.raw_object["bot_name"]
        self.action = self.raw_object["action"]
        self.conditions = self.raw_object["conditions"]