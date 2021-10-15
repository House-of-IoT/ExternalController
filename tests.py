
from relation_manager import RelationManager
from server import Server
import json
import unittest


class MockRelationManager:
    def __init__(self):
        self.relations = []
        
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
        

if __name__ == "__main__":
    unittest.main()