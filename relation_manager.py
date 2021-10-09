import json
from typing import KeysView

"""
To Change?
We are storing the device name twice after organization of bots
via organize_bots_to_minimize_searching -> Fn() . This is a minimal
improvement on storage consumption.
"""

class RelationManager:
    def __init__(self,parent):
        self.relations = self.get_relations()
        self.all_conditions_satisfied = None
        self.bots = {}
        self.parent = parent

    async def check_passive_data_for_matching_conditions_and_execute_actions(self,passive_data):
        self.organize_bots_to_minimize_searching(passive_data)
        self.all_conditions_satisfied = True
        # for every relation
        for relation in self.relations:
            #check each relation's condition to see if it is met
            for condition in relation["conditions"]:
                name = condition["bot_name"]
                keys = condition.keys()
                for key in keys:
                    if key != "device_name":
                        if self.condition_present_in_passive_data(key,condition[key],name) == False:
                            self.all_conditions_satisfied = False
                
    """
    Background: We recieve a list of objects from the server that are the bots.

    We re-organize the  data(linear complexity) with the keys representing the 
    bot data and then have constant time look up on the bot data. 
    """
    def organize_bots_to_minimize_searching(self,bot_data):
        passive_data = json.loads(bot_data)
        for bot in passive_data["bots"]:
            #ignore all deactivated bots
            if bot["active_status"] == True:
                name = bot["device_name"]
                self.bots[name] = bot

    def get_relations(self):
        file = open("relations.json","r") 
        file_data = file.read()
        file.close()
        relation_data =  json.loads(file_data)
        return relation_data["relations"]

    def condition_present_in_passive_data(self,key,value,bot_name):
        if bot_name in self.bots:
            if key in self.bots[bot_name] and self.bots[bot_name][key] == value:
                return True
            else:
                return False
        else:
            return False
    
    async def execute_action_if_conditions_were_satisfied(self,action):
        pass
