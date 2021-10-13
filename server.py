import asyncio
import json
from os import name
from config import gather_config
from last_executed_relation import LastExecuted
import queue

class Server:
    def __init__(self,parent,relations):
        self.relations = relations
        self.last_executed_relational_actions = queue.Queue(5)
        self.parent = parent
        self.devices = {}
        self.config = gather_config("hoi_s_pw")

    async def authenticate_client_after_connection(self,websocket,path):
        await websocket.send("password")
        gathered_password = await asyncio.wait_for(websocket.recv(),30)
        await websocket.send("name")
        gathered_name = await asyncio.wait_for(websocket.recv(),30)
        if  self.is_successfully_authenticated(gathered_name,gathered_password):
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
            if message == "add_relation" or message == "remove_relation":
                await self.gather_relation_and_add(websocket)
            elif message == "remove_all_relations":
                pass
            else:#viewing relations
                pass

    def relation_is_valid(self,relation):
        try:
            if "action" in relation and "device_name" in relation:
                return True
            else:
                return False
        except Exception as e:
            print(e)
            return False

    async def gather_relation_and_add(self,websocket):
        relation = await asyncio.wait_for(websocket.recv(),15)
        relation = json.loads(relation)
        
        #only add relation if the relation is proven to be valid
        if(self.relation_is_valid(relation)): 
            self.relations.append(relation)
            self.update_other_relation_copies()
            await asyncio.wait_for(websocket.send("success"),10)
        else:
            await asyncio.wait_for(websocket.send("issue"),10)

    def update_other_relation_copies(self):
        self.parent.relation_manager.relations = self.relations
        with open("relations.json","w") as File:
            File.write(json.dumps(self.relations))
        
    def add_or_replace_last_executed_relation(self,relation):
        if self.last_executed_relational_actions.qsize() == 5:
            self.last_executed_relational_actions.get()
            self.last_executed_relational_actions.put(relation)

        else:
            self.last_executed_relational_actions.put(relation)
