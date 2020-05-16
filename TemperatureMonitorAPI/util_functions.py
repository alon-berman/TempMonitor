import configparser
import glob
import json
import logging
import os
import shutil
import tempfile


def init_logger(logger_name='api_object', log_file_name='nessapi.log'):
    """
    A simple logger to log all info printed into a file.
    :return:
    """
    logger = logging.getLogger(logger_name)
    sh_handler = logging.StreamHandler()
    fh_handler = logging.FileHandler(filename=log_file_name)
    formatter = logging.Formatter(
        '%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
    sh_handler.setFormatter(formatter)
    fh_handler.setFormatter(formatter)
    logger.addHandler(sh_handler)
    logger.addHandler(fh_handler)
    logger.setLevel(logging.INFO)
    return logger


def parse_json(path):
    """
    simple function to parse a json file
    :param logger:
    :param path: path to file including suffix.
    :return: parsed json object
    """
    try:
        with open(path, 'r', encoding='cp437') as file:
            test_data = file.read()
        return json.loads(test_data)
    except Exception as e:
        print('Failed to load JSON file!. details: {}\n System will now terminate....'
              .format(e.__str__()))


def get_file_size_mb(file):
    """
    :param file: path of the file to be checked
    :return: file size in MB
    """
    return os.path.getsize(file) / 1000000  # return file size in MB


def parse_api_cfg(path):
    """
    parses .ini config file and returns it as an object
    :param path:
    :return:
    """
    cfg = configparser.ConfigParser()
    cfg.read(path)
    return cfg


def temp_file_cleanup():
    """
    cleans temp files generated during run
    :return:
    """
    [shutil.rmtree(file) for file in glob.glob(os.path.join(tempfile.gettempdir(),
                                                            '*.ness_tmp'))]
