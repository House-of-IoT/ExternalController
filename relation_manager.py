import json


class RelationManager:
    def __init__(self):
        self.relations = self.get_relation()

    def check_passive_data_for_matching_conditions_and_execute_actions(self,data):
        pass

    def get_relations(self):
        pass

    def condition_present_in_passive_data(self,key,value,data,bot_name):
        if bot_name in data:
            if key in data and data[key] == value:
                return True
            else:
                return False
        else:
            return False
