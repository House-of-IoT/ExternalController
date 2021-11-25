import websockets
import unittest
import json

class AsyncTests(unittest.IsolatedAsyncioTestCase):
    
    async def connect_to_general_server(self):
        websocket = await websockets.connect(
            'ws://localhost:50223', ping_interval= None, max_size = 20000000)
        await websocket.send("")
        await websocket.send(self.name_and_type())
        await websocket.send("test_name")
        connection_response = await websocket.recv()
        self.assertEqual(connection_response,"success")
        return websocket

    async def connect_to_external_monitor(self):
        websocket = await websockets.connect(
            'ws://localhost:50224',ping_interval= None, max_size = 20000000)
        credentials = json.dumps({"name":"test_non_bot", "password":""})
        await websocket.send(credentials)
        response = await websocket.recv()
        self.assertEqual(response,"success")
        
    async def test(self):
        external_monitor_websocket = await self.connect_to_external_monitor()
        general_server_websocket = await self.connect_to_general_server()
        
    def name_and_type(self):
        data = {"name":"test_non_bot", "type":"non-bot"}
        return json.dumps(data)