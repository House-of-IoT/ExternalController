
from relation_manager import RelationManager
import json
import unittest
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
                {"bot_name":"water_valve", "action":"open", "conditions":[{"bot_name":"soil_monitor", "humidity":2}]}
            ]
        }
        with open("relations.json","w") as File:
            File.write(json.dumps(mock_relation_config))

if __name__ == "__main__":
    unittest.main()