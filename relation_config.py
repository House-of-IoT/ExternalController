import json

class RelationConfig:
    def __init__(self):
        pass

    def prompt_and_gather_relations(self):
        relations = []
        conditions  = []
        
        while True:
            conditions = []
            device_name = input("what is the device for this new relation?:")
            action = input(f"What action should be triggered in this relation for {device_name}?:")
            while True:
                parameter_name = input("what is parameter name for this condition?:")
                parameter_value = input("what is the parameter value for this condition?:")
                device_name_for_condition = input("what is the device for this condition?:")
                conditions.append({"device name":device_name_for_condition, parameter_name:parameter_value})
                more_conditions = input("would you like to setup more conditions?[y/n]:")
                if more_conditions != "y" and more_relations != "Y":
                    break
            relations.append({"device_name":device_name, "action":action, "conditions":conditions})
            more_relations  = input("Would you like to continue creating more relations?[y/n]:")
            if more_relations != "y" and more_relations != "Y":
                break
        self.write_relations(relations)

    def write_relations(self,relations):
        data_dict = {'relations': relations}
        with open("relations.json","w") as File:
            File.write(json.dumps(data_dict))