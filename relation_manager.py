import json

"""
To Change?
We are storing the device name twice after organization of bots
via organize_bots_to_minimize_searching -> Fn() . This is a minimal
improvement on storage consumption.
"""

class RelationManager:
    def __init__(self):
        self.relations = self.get_relations()
        self.bots = {}

    async def check_passive_data_for_matching_conditions_and_execute_actions(self,passive_data):
        pass

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
        relations = []
        file = open("relations.json","r") 
        file_data = file.read()
        relation_data =  json.loads(file_data)
        for relation in relation_data["relations"]:
            relations.append(relation)
        return relations

    def condition_present_in_passive_data(self,key,value,bot_name):
        if bot_name in self.bots:
            if key in self.bots[bot_name] and self.bots[bot_name][key] == value:
                return True
            else:
                return False
        else:
            return False