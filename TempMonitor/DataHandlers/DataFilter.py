import json


def json_filter(raw_data, field: str, val=None):
    """
    this function accepts either json string or dict and returns the filtered data
    :param raw_data: str or dict
    :param field: which field to extract
    :param val: optional. Finds the field with val
    :return:
    """
    if type(raw_data) is str:
        raw_data = json.loads(raw_data)

    if val is None:
        return raw_data[field]
    else:
        return list(filter(lambda x: x[field] == val, raw_data)) #[data for data in field_data ]