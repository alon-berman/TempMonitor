from MeasurementHandler.TemperatureHandler import TemperatureHandler


class DeviceMontior:
    def __init__(self, device_id: str, temp_thresh: tuple, temp_stabilization_thresh, min_battery_volt_alert: float):
        # Client-configured Parameters
        self.device_id = device_id
        self.temp_thresh = temp_thresh
        self.temp_stabilization_thresh = temp_stabilization_thresh
        self.min_battery_volt_alert = min_battery_volt_alert
        self.measurement_handlers = []

    def prepare_run(self):
        pass

