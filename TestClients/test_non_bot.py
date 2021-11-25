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
            "device_name":"test_bot_execute", 
            "action":"test_trigger", 
            "conditions":[
                {"device_name":"test_bot_read", 
                "test_field":True}]}
        external_monitor_websocket = await self.connect_to_external_monitor()
        general_server_websocket = await self.connect_to_general_server()

    async def add_relation(self,websocket,relation):
        response = await self.add_or_remove_relation(websocket,relation,"add_relation")
        self.assertEqual(response,"success")
        response_dict = await self.execute_basic_request_reponse(websocket,"view_relations")
        self.assertEqual(response_dict["type"],"current_relations")
        self.compare_relations(relation,response_dict["relation"])
        
    async def remove_relation(self,websocket,relation):
        response = await self.add_or_remove_relation(websocket,relation,"remove_relation")
        self.assertEqual(response,"success")
        response_dict = await self.execute_basic_request_reponse(websocket,"view_relations")
        self.assertEqual(response_dict["type"],"current_relations")
        self.assertEqual(len(response_dict["relations"]),0)
    
    async def check_recent_executed_relations(self,websocket,relation):
        response_dict = await self.execute_basic_request_reponse(websocket,"view_last_relations")
        self.assertEqual(response_dict["type"],"last_executed")
    
    #make request with generic data(password and opcode) and gathers repsonse
    async def execute_basic_request_reponse(self,websocket,opcode):
        request = {"request":opcode,"password":""}
        await websocket.send(json.dumps(request))
        response = await websocket.recv()
        response_dict = json.loads(response)
        self.assertEqual(response_dict["status"],"success")
        return response_dict

    async def compare_relations(self,original_relation,gathered_relation):
        original_conditions = original_relation["conditions"]
        gathered_conditions = gathered_relation["conditions"]
        self.assertEqual(original_relation["device_name"], gathered_relation["device_name"])
        self.assertEqual(original_relation["action"], gathered_relation["action"])
        self.assertEqual(len(original_conditions),len(gathered_conditions))

        """
        The conditions gathered should reside at the same index as 
        the original one sent, since the service doesn't change the 
        order of the indexes in memory.
        """
        for i in range(len(original_conditions)):
            current_original_condition = original_conditions[i]
            current_gathered_condition = gathered_conditions[i]

            for key in current_original_condition.keys():
                original_value = current_original_condition[key]
                gathered_value = current_gathered_condition[key]
                self.assertEqual(original_value,gathered_value)

    async def add_or_remove_relation(self,websocket,relation,op_code):
        request = {"request":op_code,"password":"", "relation":relation}
        await websocket.send(json.dumps(request))
        response = await websocket.recv()
        return response

    def name_and_type(self):
        data = {"name":"test_non_bot", "type":"non-bot"}
        return json.dumps(data)