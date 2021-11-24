import hoi_client
import asyncio
import websockets

"""
Handles connection to the general server
and directly calls the relation_manager's 
passive data checking methods.
"""

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
        self.parent.good_to_execute = True

    async def gather_data_and_analyze(self):
        try:
            if self.parent.good_to_execute:
                await asyncio.wait_for(self.websocket.send("passive_data"),20)
                message = await asyncio.wait_for(self.websocket.recv(),10)
                await self.parent.relation_manager.check_passive_data_for_matching_conditions_and_execute_actions(message)
            await asyncio.sleep(5)
        except Exception as e:
            if e is websockets.WebSocketException.ConnectionClosed:
                self.parent.good_to_execute = False 
                #this has internal Exception handling.
                await self.parent.general_server_client.establish_websocket_connection()

