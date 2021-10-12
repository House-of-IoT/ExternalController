import json

class ServerConfig:

    @staticmethod
    def set_config():
        data_dict = {}
        data_dict["host"] = input('host:\n')
        data_dict["port"] = int(input("port:\n"))
        data_dict["name"] = input("name:\n")
        data_dict["type"] = input("type")
        
        with open("server_config.json" , "w") as File:
            data_to_write = json.dumps(data_dict)
            File.write(data_to_write)
