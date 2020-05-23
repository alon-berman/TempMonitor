from MeasurementHandler.AbsMeasurementHandler import AbsMeasurementHandler


class TemperatureHandler(AbsMeasurementHandler):
    def __init__(self, threshold: list):
        super().__init__()
        self.latest_measurement = None
        self.measurement_buffer = []
        self.threshold = threshold

    def check_measurement(self):
        pass

    def get_latest_measurement(self):
        return self.latest_measurement

    def get_measurement_buffer(self):
        return self.measurement_buffer