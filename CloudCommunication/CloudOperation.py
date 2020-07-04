
from CloudCommunication.TzoneInterface import TzoneHandler


def assign_cloud_object(cloud_data, logger_name='root', **kwargs):
    """
    this function assign the proper cloud object depend on cloud type provided. e.g, tzone.
    :param cloud_data:
    :param logger_name:
    :param kwargs: cloud configuration (address, keys, et cetera).
    :return: cloud object
    """
    if cloud_data["type"] == "tzone":
        return TzoneHandler(logger_name, './CloudCommunication/Config/tzone_cloud.ini', **kwargs)


