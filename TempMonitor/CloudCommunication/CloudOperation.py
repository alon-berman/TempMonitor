from CloudCommunication.TzoneInterface import TzoneHandler


def assign_cloud_object(cloud_data, logger, **kwargs):
    """
    this function assign the proper cloud object depend on cloud type provided. e.g, tzone.
    :param cloud_data:
    :param logger:
    :param kwargs: cloud configuration (address, keys, et cetera).
    :return: cloud object
    """
    if cloud_data["type"] == "tzone":
        return TzoneHandler(logger)
