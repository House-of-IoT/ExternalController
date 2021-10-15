
from relation_manager import RelationManager
from server import Server
import json
import unittest
from unittest import IsolatedAsyncioTestCase

"""Making utilization of mock classes to simulate the actual logic and test the side effects."""

class MockRelationManager:
    def __init__(self):
        self.relations = []

class MockWebsocket:
    async def recv():
        pass
    async def send(data):
        pass

class Tests(unittest.TestCase):

    def tests(self):
        #check that relations are being picked up from the config file
        self.generate_static_relation_config()
        relation_handler = RelationManager()
        self.assertEqual(len(relation_handler.relations),1)

        #check passive_data logic
        passive_data = json.dumps({"bots" : [{"device_name":"soil_monitor", "active_status":True, "humidity":2}]})
        relation_handler.organize_bots_to_minimize_searching(passive_data)
        condition_present = relation_handler.condition_present_in_passive_data("humidity",2,"soil_monitor")
        self.assertTrue(condition_present)

        #other tests
        self.relation_validation()
        self.removing_all_relations()

    def generate_static_relation_config(self):
        mock_relation_config = {
            "relations" : [
                {"device_name":"water_valve", "action":"open", "conditions":[{"device_name":"soil_monitor", "humidity":2}]}
            ]
        }
        with open("relations.json","w") as File:
            File.write(json.dumps(mock_relation_config))

    def relation_validation(self):
        server = Server(self,[])
        
        good_test_relation =  {"device_name":"water_valve", "action":"open", "conditions":[{"device_name":"soil_monitor", "humidity":2}]}
        bad_test_relation =  {"device_name":"water_valve", "action":"open"}

        good_relation_is_valid = server.relation_is_valid(good_test_relation)
        bad_relation_is_valid = server.relation_is_valid(bad_test_relation)

        self.assertTrue(good_relation_is_valid)
        self.assertFalse(bad_relation_is_valid)
    
    def removing_all_relations(self):
        server = Server(self,[])

        #mock manager for the test(server needs it for updating copies of the relations held in memory)
        self.relation_manager = MockRelationManager()

        good_test_relation =  {"device_name":"water_valve", "action":"open", "conditions":[{"device_name":"soil_monitor", "humidity":2}]}
        server.relations = [good_test_relation]
        server.update_other_relation_copies()

        #check that the relation is present inside before deletion
        relations = self.gather_relations_from_config()
        self.assertEqual(relations[0],good_test_relation)
        
        server.remove_all_relations()
        
        #check that the relation is deleted 
        relations = self.gather_relations_from_config()
        self.assertEqual(len(relations),0)

    def gather_relations_from_config(self):
        with open("relations.json","r") as File:
            data =  File.read()
            relations = json.loads(data)
            return relations
        
class AsyncTests(IsolatedAsyncioTestCase):

    async def test(self):
        self.last_executed_relation()
    
    def overwrite_relation_config(self,data):
        with open("relations.json","w") as File:
            File.write(json.dumps({"relations" : data}))

    async def last_executed_relation(self):
        mock_passive_data = json.dumps({"bots" : [{"device_name":"soil_monitor", "active_status":True, "humidity":2}]})

        #making sure the config file is setup correctly
        self.overwrite_relation_config([{"device_name":"water_valve", "action":"open", "conditions":[{"device_name":"soil_monitor", "humidity":2}]}])

        #server(required to be in the parent of relation_manager)
        self.server = Server(self,[])
        
        #to be tested
        self.relation_manager = RelationManager(self)

        #websocket(required to be in the parent of relation_manager)
        self.websocket = MockWebsocket()
        
        #passing mock passive data to simulate condition checking
        await self.relation_manager.check_passive_data_for_matching_conditions_and_execute_actions(mock_passive_data)
        
        #check side effects(server should be mutated by the relation_manager)
        self.assertEqual(len(self.server.last_executed_relational_actions),1)
        await self.relation_manager.check_passive_data_for_matching_conditions_and_execute_actions(mock_passive_data)

        #continue checking side effects and fill up the queue to test overwritting
        self.assertEqual(len(self.server.last_executed_relational_actions),2)
        await self.relation_manager.check_passive_data_for_matching_conditions_and_execute_actions(mock_passive_data)
        self.assertEqual(len(self.server.last_executed_relational_actions),3)
        await self.relation_manager.check_passive_data_for_matching_conditions_and_execute_actions(mock_passive_data)
        self.assertEqual(len(self.server.last_executed_relational_actions),4)
        await self.relation_manager.check_passive_data_for_matching_conditions_and_execute_actions(mock_passive_data)
        self.assertEqual(len(self.server.last_executed_relational_actions),5)

        queue_in_list_form = list(self.server.last_executed_relational_actions)

        #make sure the oldest  item is always getting overwritten. We only keep record of the newest executed relations
        oldest_executed_relation = queue_in_list_form[0]
        
        await self.relation_manager.check_passive_data_for_matching_conditions_and_execute_actions(mock_passive_data)
        self.assertEqual(len(self.server.last_executed_relational_actions),5)

        second_capture_of_oldest_executed_relation = self.server.last_executed_relational_actions.get()

        #the oldest item should be the second excecuted relation since the first one should have gotten overwritten.
        self.assertFalse(oldest_executed_relation.time_data == second_capture_of_oldest_executed_relation.time_data)
        self.assertFalse(oldest_executed_relation.relation["action"] == second_capture_of_oldest_executed_relation.relation["action"]) 
        self.assertFalse(oldest_executed_relation.relation["device_name"] == second_capture_of_oldest_executed_relation.relation["device_name"]) 

        self.assertEqual(self.server.last_executed_relational_actions.qsize ,5)


if __name__ == "__main__":
    unittest.main()