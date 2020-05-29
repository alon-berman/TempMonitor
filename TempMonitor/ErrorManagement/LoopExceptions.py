class BaseLoopException(Exception):
    pass


class CloudException(BaseLoopException):
    pass


class NoInternetException(BaseLoopException):
    pass


class LanguageNotFound(BaseLoopException):
    pass

class TemperatureExceededError(BaseLoopException):
    pass