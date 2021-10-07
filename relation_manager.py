import json

class RelationManager:
    def __init__(self):
        self.relations = self.get_relations()

    def check_passive_data_for_matching_conditions_and_execute_actions(self,data):
        pass

    def get_relations(self):
        relations = []
        file = open("relations.json","r") 
        file_data = file.read()
        relation_data =  json.loads(file_data)
        for relation in relation_data["relations"]:
            relations.append(relation)
        return relation

    def condition_present_in_passive_data(self,key,value,data,bot_name):
        if bot_name in data:
            if key in data and data[key] == value:
                return True
            else:
                return False
        else:
            return False
