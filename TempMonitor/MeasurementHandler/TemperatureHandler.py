from time import sleep
import numpy as np
from ErrorManagement.LoopExceptions import TemperatureExceededError
from MeasurementHandler.AbsMeasurementHandler import AbsMeasurementHandler

_BUFF_SIZE = 30


class TemperatureHandler(AbsMeasurementHandler):
    def __init__(self, handler_cfg: dict,
                 get_data, device_id, logger):
        """
        temperature monitor object that ideally runs as a thread of a device object.
        it continously monitorsof
        :param handler_cfg:
        :param get_data:
        :param device_id:
        :param logger:
        """
        super().__init__()
        self.logger = logger
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
        self.logger.debug(f'device {self.device_id} buffer: {self.measurement_buffer} \n')
        if self.is_temp_stabilized():
            current_temperature = self.get_data_func(self.device_id)
            self._update_buffer(current_temperature)
            if current_temperature not in np.arange(self.threshold[0], self.threshold[1]):
                raise TemperatureExceededError
            else:
                self.logger.debug('Temperature within threshold')
        else:
            self.logger.debug('Temperature is yet to be stabilized!')

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
        if abs(self.measurement_buffer[-2] - self.measurement_buffer[-1]) > self.stabilization_threshold_c:
            self.logger.debug('Waiting for temp to stabilize...')
            return False
        return True

    def _update_buffer(self, curr_temp):
        self.logger.debug('Waiting for temp to stabilize...')
        if len(self.measurement_buffer) == _BUFF_SIZE:
            self.measurement_buffer.pop(0)
        self.measurement_buffer.append(curr_temp)

    def _loop(self):
        while True:
            sleep(self.time_interval_sec)
            self._update_buffer(self.get_data_func(self.device_id))
            try:
                self.check_measurement()
            except TemperatureExceededError:
                self.logger.debug('Temperature Exceeded!')