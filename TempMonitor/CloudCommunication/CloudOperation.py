from CloudCommunication.TzoneInterface import TzoneHandler


def assign_cloud_object(cloud_type: str, *args):
    """
    this function assign the proper cloud object depend on cloud type provided. e.g, tzone.
    :param cloud_type: string
    :param args: object input args.
    :return: cloud object
    """
    if cloud_type == "tzone":
        return TzoneHandler(*args)


