import asyncio
import json
from os import name
from config import gather_config
from last_executed_relation import LastExecuted
from datetime import datetime
import queue

class Server:
    def __init__(self,parent,relations):
        self.relations = relations
        self.last_executed_relational_actions = queue.Queue(5)
        self.parent = parent
        self.devices = {}
        self.config = gather_config(file_name = "server_config.json",env_pw_name="hoi_s_pw")

    async def authenticate_client_after_connection(self,websocket,path):
        await websocket.send("password")
        gathered_password = await asyncio.wait_for(websocket.recv(),30)
        await websocket.send("name")
        gathered_name = await asyncio.wait_for(websocket.recv(),30)

        if self.is_successfully_authenticated(gathered_name,gathered_password):
            self.devices[gathered_name] = websocket
            await self.main_loop(websocket,name)
        else:
            await asyncio.wait_for(websocket.send("issue"),10)
    
    def is_successfully_authenticated(self,name,user_password):
        if user_password == self.config["password"] and name not in self.devices:
            return True
        else:
            return False

    async def main_loop(self,websocket,name):
        while name in self.devices:
            message = await websocket.recv()
            message = json.loads(message)

            if message["request"] == "add_relation" or message["request"] == "remove_relation":
                await self.add_or_remove_relation(websocket,message["relation"],message["request"])

            elif message["request"] == "remove_all_relations":
                self.remove_all_relations()
                await asyncio.wait_for(websocket.send("success"),10)

            else:#viewing relations
                await self.send_last_execute_relations(websocket)

    def relation_is_valid(self,relation):
        try:
            if "action" in relation and "device_name" in relation and "conditions" in relation and len(relation["conditions"])>0:
                return True
            else:
                return False
        except Exception as e:
            print(e)
            return False

    async def add_or_remove_relation(self,websocket,relation,request):
        #only add/remove relation if the relation is proven to be valid
        if(self.relation_is_valid(relation)): 
            if request == "add_relation":
                self.relations.append(relation)
                self.update_other_relation_copies()
            else:
                self.find_and_remove_relation(relation)
            await asyncio.wait_for(websocket.send("success"),10)
        else:
            await asyncio.wait_for(websocket.send("issue"),10)

    def update_other_relation_copies(self):
        self.parent.relation_manager.relations = self.relations
        with open("relations.json","w") as File:
            File.write(json.dumps(self.relations))
        
    def add_or_replace_last_executed_relation(self,relation):
        last_executed = LastExecuted(relation,datetime.utcnow())
        if self.last_executed_relational_actions.qsize() == 5:
            #remove the oldest  from the queue and add the new one
            self.last_executed_relational_actions.get()
            self.last_executed_relational_actions.put(last_executed)

        else:
            self.last_executed_relational_actions.put(last_executed)

    async def send_last_execute_relations(self,websocket):
        list_last_executed = list(self.last_executed_relational_actions)
        json_list_last_executed = json.dumps(list_last_executed)
        await asyncio.wait_for(websocket.send(json_list_last_executed))

    def find_and_remove_relation(self,target_relation):
        for relation in self.relations:
            #there can only be one relation with a unique action/device name.
            if relation["action"] == target_relation["action"] and relation["device_name"] == target_relation["device_name"]:
               self.relations.remove(relation)
               break

    def remove_all_relations(self):
        with open("relations.json","w") as File:
            File.write(json.dumps({"relations":[]}))