import json
import threading
from time import time, sleep
import datetime

from urllib3.exceptions import ProtocolError

from CloudCommunication.CloudUtilities import get_request
from CloudCommunication.Config.operation.ini import read_ini_cfg
from CloudCommunication.AbstractCloudObject import AbsCloudObj
from DataHandlers.DataFilter import json_filter
from ErrorManagement.CloudExceptions import CloudNoDataException
from ErrorManagement.Logger import configure_logger
from ErrorManagement.ProgramFlowExceptions import SameMeasurementError


class TzoneHandler(AbsCloudObj):
    def __init__(self, business_logger, ini_config_path, **kwargs):
        super().__init__()
        self.logger = business_logger
        self.num_attempts = 0
        self.cfg = read_ini_cfg(ini_config_path)
        self.data = (None, None)  # (time of data acquisition, cloud data)
        self.data_update_thread = threading.Thread(target=self.get_raw_data_loop)
        self.prepare_run()

    def get_latest_device_data(self):
        pass

    def prepare_run(self):
        self.update_raw_data()
        self.data_update_thread.start()

    def get_raw_data_loop(self):
        while True:
            sleep(eval(self.cfg['data']['data_refresh_time_sec']))
            try:
                self.update_raw_data()

            except KeyError:
                if self.num_attempts > int(self.cfg['connectivity']['max_retries']):
                    self.logger.debug('Failed to get raw data from Tzone Cloud, attempt {}/{}'
                                      .format(self.num_attempts, self.cfg['connectivity']['max_retries']))
                    self.num_attempts = 0
                    raise CloudNoDataException
                else:
                    self.num_attempts += 1

    def get_device_data(self, device_id: str, timestamp_to_compare: str):
        try:
            # Set time-Xs in tzone cloud format
            begin_time = tzone_date_formatter(eval(self.cfg['data']['data_refresh_time_sec']))
            # create cloud request
            body = prepare_cloud_request(device_id, begin_time)
            req = get_request('POST',
                              self.cfg['connectivity']['cloud_url'],
                              eval(self.cfg['connectivity']['request_header']),
                              body)
            data = tzone_cloud_data_to_json(req.data, self.cfg['data']['data_key'])
            self.logger.debug('data : {}'.format(data.encode('UTF-8')))
            if data['ResultList']['RTC'] == timestamp_to_compare:
                raise SameMeasurementError
            else:
                return data['ResultList']
        except IndexError:
            self.logger.warning('Index Error raised!')
            self.get_device_data(device_id,timestamp_to_compare)

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
            if data:
                return float(data[0][field].split(separator)[0])
            else:
                return None
        except TypeError:
            return None

    def update_raw_data(self):
        start = time()
        begin_time = tzone_date_formatter(eval(self.cfg['data']['data_refresh_time_sec']))
        body = prepare_cloud_request(begin_time)
        try:
            req = get_request('POST',
                              self.cfg['connectivity']['cloud_url'],
                              eval(self.cfg['connectivity']['request_header']),
                              body)
            data = tzone_cloud_data_to_json(req.data, self.cfg['data']['data_key'])
        except ProtocolError:
            data = self.data(0)
            self.logger.WARNING('Connection Forcibly Closed, Trying again..')
        self.logger.debug(f'Cloud Data Acquisiton Time Elapsed : {time() - start} seconds')
        self.data = (start, data)


def prepare_cloud_request(device_id,
                          begin_time,
                          end_time=None,
                          allow_paging=True,
                          num_results=1,
                          total_count=0,
                          page_index=1,
                          m='GetTAG04'):
    """

    :param m: Something unclear.
    :param device_id: requested device id
    :param begin_time: date string in YYYY-MM-DD HH MM SS. see date_formatter function for assistance.
    :param end_time: same format as mentioned above. Default is now.
    :param allow_paging: Boolean
    :param num_results: refers to PageSize. how many results should be contained in each "page"
    :param total_count:
    :param page_index: how many pages should divide the result
    :return: A dictionary of an acceptable POST request for TZone Cloud
    """
    if end_time is None:
        end_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    return {
        "BeginTime": begin_time,
        "EndTime": end_time,
        "AllowPaging": allow_paging,
        "PageSize": f"{num_results}",
        "TotalCount": total_count,
        "PageIndex": page_index,
        "M": m,
        "sn": device_id
    }


def tzone_date_formatter(seconds):
    dt = datetime.datetime.now() - datetime.timedelta(seconds=seconds)
    return dt.strftime("%Y-%m-%d %H:%M:%S")


def tzone_cloud_data_to_json(json_string, data_key):
    return json.loads(json_string)[data_key]

if __name__ == '__main__':
    logger = configure_logger()
    h = TzoneHandler(logger, )
    print(h.get_device_data("06190229"))
