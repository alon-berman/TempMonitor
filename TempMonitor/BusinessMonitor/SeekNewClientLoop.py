import os
import json
from time import sleep
from BusinessMonitor.MonitorObject import BusinessMonitor
from ErrorManagement.LoopExceptions import LoopException
import multiprocessing as mp


def loop():

    business_processes = []
    running_clients = []
    while True:
        clients_as_json = os.listdir('../ClientData')
        for client in clients_as_json:
            if client in running_clients:
                break
            else:
                client_file_path = "..\\ClientData\\{}".format(client)
                try:
                    if 'test_' not in client:
                        with open(client_file_path) as client_data:
                            biz = json.load(client_data)[0]
                            print("Initiating {} To Processes List ....".format(biz["business_details"]["business_name"]))
                            business_process = mp.Process(name=client, target=BusinessMonitor, kwargs=biz)
                            business_process.start()
                            business_processes.append(business_process)
                            running_clients.append(client)
                except LoopException as le:
                    le.__init__("Couldn't instantiate process of {}".format(client_file_path))
            sleep(0.5)


if __name__ == '__main__':
    print("Montior Starts ...")
    loop()