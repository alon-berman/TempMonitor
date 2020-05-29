import json
from time import sleep
from bs4 import BeautifulSoup

from CloudCommunication.AbstractCloudObject import AbsCloudObj
from CloudCommunication.browser import Browser
from DataHandlers.DataFilter import json_filter
from ErrorManagement.CloudExceptions import CloudNoDataException
from ErrorManagement.Logger import configure_logger

CLOUD_URL = r'http://t-open.tzonedigital.cn/'
WEB_LOAD_TIME = 5
MAX_RETRIES = 10


class TzoneHandler(AbsCloudObj):
    def __init__(self, logger):
        super().__init__()
        self.logger = logger
        self.num_attempts = 0
        self.browser = Browser()

    def get_raw_data(self):
        try:
            with self.browser as browser:
                browser.get(CLOUD_URL)
                sleep(WEB_LOAD_TIME)
                html = browser.page_source


            page_soup = BeautifulSoup(html, 'html.parser')
            sleep(2.01)  # Suppress Request frequency too fast (less than 2 seconds)
            raw_cloud_data = page_soup.findAll("table", {"id": "tab1"})[0].attrs['jsondata']
            self.logger.debug('raw cloud data' + raw_cloud_data)
            return json.loads(raw_cloud_data)

        except KeyError:
            if self.num_attempts > MAX_RETRIES:
                self.logger.debug('Failed to get raw data from Tzone Cloud, attempt {}/{}'
                                  .format(self.num_attempts, MAX_RETRIES))
                self.num_attempts = 0
                raise CloudNoDataException
            else:
                self.num_attempts += 1
                self.get_raw_data()

    def get_device_data(self, device_id: str):
        try:
            raw_data = self.get_raw_data()
            if raw_data is None:
                return None
            filtered_data = json_filter(
                raw_data,
                "SN", device_id
            )
            # self.logger.debug('filtered_data : {}'.format(filtered_data.encode('UTF-8'))
            return filtered_data

        except IndexError:
            self.logger.warning('Index Error raised!')
            self.get_device_data(device_id)

    def get_device_voltage(self, device_id: str):
        data = self.data_formatter(device_id, 'VBV', 'V')
        self.logger.debug('get_device_voltage: {}'.format(data))
        return data

    def get_device_temperature(self, device_id):
        data = self.data_formatter(device_id, 'Temperature', '℃')
        self.logger.debug('got temperature: {} \n'.format(data))
        return data

    def data_formatter(self, device_id, field, separator):
        data = self.get_device_data(device_id)
        try:
            return float(data[field].split[separator][0])
        except TypeError:
            return None


if __name__ == '__main__':
    logger = configure_logger()
    h = TzoneHandler(logger)
    print(h.get_device_data("06190229"))