
from general_server_client import GeneralServerClient
from server import Server
from config import gather_config
from relation_manager import RelationManager
import websockets
import asyncio

class Main:
    def __init__(self):
        self.good_to_execute = False
        self.config = gather_config()
        self.general_server_client = GeneralServerClient()
        self.relation_manager = RelationManager(self)
        self.server = Server(self,self.relation_manager.relations)

    def start(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.general_server_client.main())
        loop.run_until_complete(
            websockets.serve(
                self.server.authenticate_client_after_connection,
                self.config.host,
                self.config.port,
                ping_interval=None))
        loop.run_forever()

if __name__ == "__main__":
    main = Main()
    main.start()