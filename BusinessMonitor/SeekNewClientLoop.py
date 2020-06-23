import multiprocessing as mp
import threading
from time import sleep

from BusinessMonitor.MonitorObject import BusinessMonitor
from ErrorManagement.Logger import configure_logger
from ErrorManagement.LoopExceptions import BaseLoopException
from MongoClient.mongo_client import MongoHandler

mongo_handler = MongoHandler().db.businesses


class MainLoop:
    instance = None

    class __MainLoop:
        def __init__(self, *args, **kwargs):
            # self.logger = configure_logger(log_to_file=True, logger_name='MainLoop', cyclic_max_bytes=1e6)
            self.args = args
            self.kwargs = kwargs
            self._loop_thread = threading.Thread(target=self.loop)
            self._loop_thread.start()

        def loop(self):

            business_processes = []
            running_clients = []
            while True:
                clients_as_json = mongo_handler.find({'is_monitored': False})
                for client in clients_as_json:
                    client_name = client["business_details"]["business_name"]
                    try:
                        # self.logger.debug("Appending {} To Processes List ....".format(client_name))
                        client_monitor = BusinessMonitor(client['business_details'],
                                                         client['devices'],
                                                         client['business_debug_mode'])
                        business_processes.append(client_monitor)
                        running_clients.append(client)
                        mongo_handler.update_one({'_id': client['_id']}, {"$set": {'is_monitored': True}})
                    except BaseLoopException as le:
                        le.__init__("Couldn't instantiate process of {}".format(client_name))
                sleep(0.5)

    def __init__(self, *args, **kwargs):
        if not self.instance:
            self.instance = MainLoop.__MainLoop(args, kwargs)
        else:
            pass
        # put here logic if instance already exists

    def __getattr__(self, name):
        return getattr(self.instance, name)
