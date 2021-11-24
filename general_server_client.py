
import hoi_client
import asyncio

class GeneralServerClient:
    def __init__(self,parent):
        self.client = hoi_client.Client()
        self.parent = parent

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
            await self.parent.relation_manager.check_passive_data_for_matching_conditions_and_execute_actions(message)
            
        except Exception as e:
           pass
