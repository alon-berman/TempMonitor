import configparser


def read_ini_cfg(ini_path: str):
    try:
        cfg = configparser.ConfigParser()
        cfg.read(ini_path)
        return cfg
    except Exception as e:
        print('Could not find file in path {}. Make sure it exists! \nDetails: {}'.format(ini_path,
                                                                                          e))