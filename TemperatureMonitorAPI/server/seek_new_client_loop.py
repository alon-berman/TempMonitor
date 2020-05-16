import os
import json
from time import sleep
from server.monitor_object import BusinessMonitor
from LoopExceptions import LoopException
import multiprocessing as mp


def loop():

    business_processes = []
    running_clients = []
    while True:
        clients_as_json = os.listdir('./client_data')
        for client in clients_as_json:
            if client in running_clients:
                break
            else:
                client_file_path = "{}\\client_data\\{}".format(os.path.dirname(os.path.abspath(__file__)), client)
                try:
                    if 'jb_tmp' not in client:
                        with open(client_file_path) as client_data:
                            biz = json.load(client_data)
                            print("Initiating {} To Processes List ....".format(biz["business_name"]))
                            business_process = mp.Process(name=client, target=BusinessMonitor, args=(biz["mqtt_server"],
                                                               biz["mqtt_port"],
                                                               biz["cloud_user"],
                                                               biz["cloud_password"],
                                                               biz["temperature"],
                                                               biz["topic_out"],
                                                               biz["debug_mode"],
                                                               biz["business_name"],
                                                               biz["log_level"],
                                                               biz["stabilization_temp"]
                                                               ))
                            business_process.start()
                            business_processes.append(business_process)
                            running_clients.append(client)
                except LoopException as le:
                    le.__init__("Couldn't instantiate process of {}".format(client_file_path))
            sleep(0.5)


if __name__ == '__main__':
    print("Montior Starts ...")
    loop()
