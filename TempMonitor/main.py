from CloudCommunication import CloudOperation
from CloudCommunication.TzoneInterface import get_raw_data
from FilterTools.JSONFilter import json_filter



def loop():
    cloud_data = get_raw_data()
    sensor_filtered_data = json_filter(cloud_data, "IMEI", "641984907900006")

if __name__ == '__main__':
    loop()

