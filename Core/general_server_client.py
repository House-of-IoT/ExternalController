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

    """
    Try to connect/authenticate and begin gathering/analyzing data.
    """
    async def main(self):
        while True:
            try:
                await self.establish_websocket_connection()      
                response = await self.client.send_connection_credentials(self.websocket)
                if response == "success":
                    loop = asyncio.get_event_loop()
                    loop.run_until_complete(self.gather_data_and_analyze())
                    break #no longer need to try to connect and authenticate
                else:
                    print("authentication failed")
            except Exception as e:
                print(e)
            await asyncio.sleep(5)

    async def establish_websocket_connection(self):
        self.websocket = self.client.establish_connection()

    async def gather_data_and_analyze(self):
        while True:
            try:
                await asyncio.wait_for(self.websocket.send("passive_data"),20)
                message = await asyncio.wait_for(self.websocket.recv(),10)
                await self.parent.relation_manager.check_passive_data_for_matching_conditions_and_execute_actions(message)
            except Exception as e:
                if e is websockets.WebSocketException.ConnectionClosed:
                    #this has internal Exception handling.
                    await self.parent.general_server_client.establish_websocket_connection()
            await asyncio.sleep(5)