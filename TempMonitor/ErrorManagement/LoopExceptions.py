import logging


class LoopException(BaseException):
    """
    It is guaranteed that LoopException will be called only once.
    Therefore, the logger init is included inside the Exceptions.
    """
    def __init__(self, msg='', business_name=''):
        self.logger = self.init_log(business_name)
        self.log_msg(msg)

    @staticmethod
    def init_log(business_name):
        logger = logging.getLogger(business_name)
        logger.setLevel(logging.DEBUG)
        return logger

    def log_msg(self, msg):
        self.logger.info(msg)

