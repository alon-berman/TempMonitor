import logging
from logging.handlers import RotatingFileHandler


def configure_logger(
        logging_level=logging.INFO,
        log_to_file=True,
        print_logging=False,
        log_output_path=None,
        cyclic_log_files=False,
        get_existing=False,
        cyclic_max_bytes=2000,
        cyclic_backup_count=10,
        logger_name='Main',
        message_format=''
):
    """
    basic initialization of logger.
    :param message_format:
    :param logging_level: int, optional
        0   - ALL     All levels including custom levels.
        10  - DEBUG	Designates fine-grained informational events that are most useful to debug an application.
        20  - INFO	Designates informational messages that highlight the progress of the application at coarse-grained level.
        30  - WARN	Designates potentially harmful situations.
        40  - ERROR	Designates error events that might still allow the application to continue running.
        50  - FATAL	Designates very severe error events that will presumably lead the application to abort.
    :param log_to_file: boolean, optional
        True- create and save the logs to a file
        False-not creating nor saving the logs to a file
    :param print_logging: boolean, optional
        True- print logs to console
        False- not printing logs to console
    :param log_output_path: string, optional
        a path to where the log file is designated, must end with '.log'
    :param cyclic_log_files:
    :param cyclic_max_bytes:
    :param cyclic_backup_count:
    :param logger_name: string, optional
        let you differ between different logs in the same log file
    :return: Logging.logger object
    """
    if message_format == '':
        message_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

    if log_output_path is None:
        log_output_path = 'Main.log'

    # bugs: - creates a file even if file output is off
    logging.basicConfig(format='%(asctime)s - %(message)s',
                        datefmt='%d-%b-%y %H:%M:%S')
                        # filename=log_output_path)

    logger = logging.getLogger(logger_name)
    if get_existing:
        return
    formatter = logging.Formatter(message_format)

    # remove all default handlers (enables print only)
    for handler in logger.handlers:
        logger.removeHandler(handler)

    # add file output
    if log_to_file:
        if cyclic_log_files:
            fh = RotatingFileHandler(
                log_output_path,
                maxBytes=cyclic_max_bytes, backupCount=cyclic_backup_count
                )

        else:
            fh = logging.FileHandler(log_output_path)

        fh.setFormatter(formatter)
        logger.addHandler(fh)
    # add print output
    if print_logging:
        terminal_handle = logging.StreamHandler()
        terminal_handle.setLevel(logging_level)
        terminal_handle.setFormatter(formatter)

        logger.addHandler(terminal_handle)

    logger.setLevel(logging_level)
    return logger


if __name__ == '__main__':
    configure_logger(logging_level=logging.INFO, cyclic_log_files=True, cyclic_max_bytes=5)
    logging.info('hi')
