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
        relation = {
            "device_name":"water_valve", 
            "action":"open", 
            "conditions":[
                {"device_name":"test_bot_execute", 
                "test_field":True}]}
        external_monitor_websocket = await self.connect_to_external_monitor()
        general_server_websocket = await self.connect_to_general_server()

    async def add_relation(self,websocket,relation):
        response = await self.add_or_remove_relation(websocket,relation,"add_relation")
        self.assertEqual(response,"success")
    
    async def remove_relation(self,websocket,relation):
        response = await self.add_or_remove_relation(websocket,relation,"remove_relation")
        self.assertEqual(response,"success")


    async def add_or_remove_relation(self,websocket,relation,op_code):
        request = {"request":op_code,"password":"", "relation":relation}
        await websocket.send(json.dumps(request))
        response = await websocket.recv()
        return response

    def name_and_type(self):
        data = {"name":"test_non_bot", "type":"non-bot"}
        return json.dumps(data)
