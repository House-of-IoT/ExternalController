import json 
import hoi_client
import os

def set_config():
    data_dict = {}
    data_dict["host"] = input('host:\n')
    data_dict["port"] = int(input("port:\n"))
    data_dict["name"] = input("name:\n")
    data_dict["type"] = input("type")
    
    with open("config.json" , "w") as File:
        data_to_write = json.dumps(data_dict)
        File.write(data_to_write)

def gather_config():
     with open("config.json" , "r") as File:
       data = json.loads(File.read())
       password = os.environ.get("hoi_mdc_pw")
       config = hoi_client.Config(data["port"],data["host"],password,data["name"],data["type"])
       return config
       
if __name__ == "__main__":
    set_config()