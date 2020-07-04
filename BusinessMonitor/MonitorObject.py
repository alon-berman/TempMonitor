import json
import logging
import multiprocessing
from time import time
from DeviceMonitor.MonitorObject import DeviceMonitor
from ErrorManagement.Logger import configure_logger

_BUFF_SIZE = 10


def load_client_details(client_details_json_path):
    with open(client_details_json_path) as f:
        return json.load(f)


class BusinessMonitor:
    """
    Each client of the service has this process running on server monitoring the temperature.

    """
    def __init__(self, business_details, devices, business_debug_mode):
        """
        :param business_details:
        :param business_debug_mode:
        :param devices:
        """
        # Init parameters
        if business_debug_mode:
            log_level = logging.DEBUG
            print_logging = True
        else:
            log_level = logging.WARNING
            print_logging = False

        self.logger = configure_logger(logger_name=business_details["business_name"],
                                       logging_level=log_level, print_logging=print_logging,
                                       log_to_file=True, cyclic_max_bytes=1e6)

        self.device_processes_list = []
        self.business_debug_mode = business_debug_mode
        self.last_email_sent_seconds = time()
        self.should_send_email = False
        self.devices = devices
        # Client Data
        self.business_details = business_details

        self.prepare_run()
        self.monitor()
        self.logger.debug('created businsess handler for {}'.format(business_details["business_name"]))

    def prepare_run(self):
        pass

    def monitor(self):
        for device in self.devices:
            if device["monitor_enabled"]:
                self.logger.debug('Entered monitor loop')
                # todo: debug DeviceMonitor Input arguments
                DeviceMonitor(**self.business_details, **device, logger_name=self.logger.name)
                # process = multiprocessing.Process(name=device["device_id"],
                #                                   target=DeviceMonitor,
                #                                   args=(self.business_details["business_name"],
                #                                         self.business_details["contact_name"],
                #                                         self.business_details["contact_email"]),
                #                                   kwargs=device)
                self.logger.debug(f'initiating DeviceMonitor process for {device["device_id"]}')
                # process.start()
                # self.device_processes_list.append(process)
            else:
                self.logger.debug(f'Skipping Monitoring of {device["device_id"]}')


if __name__ == '__main__':
    pass
    # monitor = BusinessMonitor("eu.thethings.network", 1883, "temp_monitor_tester",
    #                           "ttn-account-v2.bznvspfhnrWpP1AkkHKw5bEsTJ-blN9Ywkx5IJQzOXY",
    #                           [-4, 50], dev_id="lht65279777", temp_stabilization_thresh=3,
    #                           debug_mode=True, min_battery_volt_alert=0.85)
    # monitor = BusinessMonitor('ClientData/home.json')