import logging


class LoopException(BaseException):
    def __init__(self, msg='', business_name=''):
        self.logger = self.init_log(business_name)
        self.log_msg(msg)

    def init_log(self, business_name):
        logger = logging.getLogger(business_name)
        logger.setLevel(logging.DEBUG)
        return logger

    def log_msg(self, msg):
        self.logger.info(msg)

