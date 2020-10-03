import logging
from time import sleep
import numpy as np
from ErrorManagement.LoopExceptions import TemperatureExceededError
from ErrorManagement.ProgramFlowExceptions import SameMeasurementError
from MeasurementHandler.AbsMeasurementHandler import AbsMeasurementHandler

_BUFF_SIZE = 5


class TemperatureHandler(AbsMeasurementHandler):
    def __init__(self, handler_cfg: dict,
                 get_data, device_id, logger_name='root'):
        """
        temperature monitor object that ideally runs as a thread of a device object.
        it constantly monitors the cloud for new queries of the device_id
        :param handler_cfg:
        :param get_data: function pointer to the sensor cloud data
        :param device_id:
        :param logger_name:
        """
        super().__init__()
        self.logger = logging.getLogger(logger_name)
        self.device_id = device_id
        self.measurement_buffer = []
        self.threshold = handler_cfg["threshold"]
        self.stabilization_threshold_c = handler_cfg["stabilization_threshold_c"]
        self.unit = handler_cfg["unit"]
        self.time_interval_sec = handler_cfg["time_interval_sec"]
        self.get_data_func = get_data
        self.logger.debug('created temperature handler for device {}'.format(device_id))
        self._loop()

    def check_measurement(self):
        self.logger.debug(f'check_measurement: device {self.device_id} buffer: {self.measurement_buffer} \n')
        data = self.get_data_func(self.device_id)
        if data:
            # check if measurement was not collected already (timestamp comparison)
            if len(self.measurement_buffer) > 0:
                if data['RTC'] == self.measurement_buffer[-1]['RTC']:
                    raise SameMeasurementError
            # if data is valid, append to measurement buffer.
            self.measurement_buffer.append(data)
            if len(self.measurement_buffer) > 1 and self.measurement_buffer[-1]['RTC'] is not None:
                # check if temperature is stable for examination
                if self.is_temp_stabilized():
                    self.logger.debug('check_measurement data returned : {}'.format(data))
                    # Check temperature excision
                    if not self.threshold[0] < data['temperature'] < self.threshold[1]:
                        raise TemperatureExceededError
                    else:
                        self.logger.debug('check_measurement: Temperature within threshold')
                else:
                    self.logger.debug('check_measurement: Temperature is yet to be stabilized!')
            else:
                self.logger.debug('check_measurement: Yet to be stabilizied')

    def get_latest_measurement(self):
        return self.measurement_buffer[-1]

    def get_measurement_buffer(self):
        return self.measurement_buffer

    def is_temp_stabilized(self):
        """
        this functions look at last two measurements from buffer and check if their
        delta is lower than the stabilization threshold set.
        :return: bool
        """
        if len(self.measurement_buffer) < 2:
            return False
        if abs(self.measurement_buffer[-2]['temperature'] - self.measurement_buffer[-1]['temperature']) >\
                self.stabilization_threshold_c:
            self.logger.debug('Waiting for temp to stabilize...')
            return False
        self.logger.debug('Temperature is stabilized...')
        return True

    def _update_buffer(self, curr_temp, time_of_measurement):
        self.logger.debug('Waiting for temp to stabilize...')
        if curr_temp is not None:
            self.measurement_buffer.append((curr_temp, time_of_measurement))

    def _loop(self):
        while True:
            sleep(self.time_interval_sec)
            try:
                if len(self.measurement_buffer) == _BUFF_SIZE:
                    self.measurement_buffer.pop(0)
                self.check_measurement()
            except TemperatureExceededError:
                self.logger.debug('Temperature Exceeded!')
            except SameMeasurementError:
                self.logger.debug('Got Same Measurement!')

