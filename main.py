import hoi_client
from config import gather_config
import asyncio

class Main:
    def __init__(self):
        self.config = gather_config()
        self.client = hoi_client.Client()

    async def main(self):
        await self.establish_websocket_connection()      
        response = await self.client.send_connection_credentials(self.websocket)
        if response == "success":
            tasks = [self.gather_data_and_analyze()]
            await self.client.main(self.websocket,tasks)
        else:
            print("authentication failed")

    async def establish_websocket_connection(self):
        self.websocket = self.client.establish_connection()

    async def gather_data_and_analyze(self):
        try:
            await asyncio.wait_for(self.websocket.send("passive_data"),20)
            message = await asyncio.wait_for(self.websocket.recv(),10)
        except:
            pass #handle
