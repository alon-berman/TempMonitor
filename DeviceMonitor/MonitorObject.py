import logging
import threading
from time import time, sleep

import numpy as np

from ClientCommunication.email import send_mail
from CloudCommunication.CloudOperation import assign_cloud_object
from ErrorManagement.LoopExceptions import CloudException, NoInternetException
from MeasurementHandler.TemperatureHandler import TemperatureHandler


class DeviceMonitor:
    def __init__(self, contact_name: str, business_name: str, contact_email: str, device_id: str,
                 tag: str, cloud_config: dict, measurement_types: dict, contact_phone: str,
                 min_battery_volt_alert: float, time_between_alerts_sec: int, debug_mode: int,
                 monitor_enabled=1, logger_name=''):
        if not monitor_enabled:
            quit()
        # System-configured Parameters
        self.business_name = business_name
        self.device_owner_name = contact_name
        self.device_owner_email = contact_email
        self.contact_phone = contact_phone
        self.last_email_sent_seconds = -np.inf
        self.should_send_email = None
        self.device_id = device_id
        self.logger = logging.getLogger(logger_name)

        # Client-configured Parameters
        self.tag = tag
        self.time_between_alerts_sec = time_between_alerts_sec
        self.min_battery_volt_alert = min_battery_volt_alert
        self.measurement_types = measurement_types
        self.measurement_handlers = []

        # Cloud Interface
        self.cloud_handler = assign_cloud_object(cloud_config,
                                                 self.logger.name)

        # Advanced
        self.debug_mode = debug_mode
        self.logger.debug('created device handler for device {}'.format(device_id))
        self.prepare_run()
        self.monitor_battery()

    def prepare_run(self):
        for meas_type in self.measurement_types:
            if meas_type == 'temperature':
                proc = threading.Thread(target=TemperatureHandler,
                                        kwargs=({
                                            "handler_cfg": self.measurement_types[meas_type],
                                            "get_data": self.cloud_handler.get_device_data,
                                            "device_id": self.device_id,
                                            "logger_name": self.logger.name
                                        }))
                proc.start()
                self.measurement_handlers.append(proc)
            if meas_type == 'humidity':
                pass

    def monitor_battery(self):
        while True:
            try:
                sleep(10*60)
                if self.is_battery_low():
                    self.logger.warning('DEVICE BATTERY VOLTAGE LOW! \n'
                                        'Device ID : {}'.format(self.device_id),
                                        )
                else:
                    self.logger.debug('Battery voltage OK')

            except NoInternetException:
                self.logger.warning('No Internet Connection could be established')
            except CloudException:
                self.logger.error('Failed to communicate with cloud')

    def is_battery_low(self):
        battery_voltage = self.get_current_battery_voltage()
        self.logger.debug(f'Measured Voltage {battery_voltage} V')
        if battery_voltage is not None\
                and (battery_voltage < self.min_battery_volt_alert):
            if self.should_send_mail:
                send_mail(self.device_owner_name,
                          self.device_owner_email,
                          'battry_low',
                          additional_msg=f'Battery is Low! {battery_voltage}V')
                self.last_email_sent_seconds = time()
        else:
            return

    def get_current_battery_voltage(self):
        return self.cloud_handler.get_device_current_voltage()

    def should_send_mail(self):
        if time() - self.last_email_sent_seconds < self.time_between_alerts_sec:
            return True
        else:
            return False
