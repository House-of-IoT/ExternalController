import asyncio
import json
from os import name
from config import gather_config

class Server:
    def __init__(self,parent,relations):
        self.relations = relations
        self.last_executed_relational_actions = None
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

    def main_loop(self,websocket,name):
        pass
