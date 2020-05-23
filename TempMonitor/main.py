from CloudCommunication import CloudOperation
from CloudCommunication.TzoneInterface import TzoneHandler
from DataHandlers.DataFilter import json_filter
from BusinessMonitor.MonitorObject import BusinessMonitor


def loop():
    cloud_handler = TzoneHandler()
    sensor_filtered_data = json_filter(cloud_handler.get_raw_data(), "IMEI", "641984907900006")
    pass


if __name__ == '__main__':
    loop()

