import json

import urllib3


def get_request(request_type: str, address: str, headers: dict, body: dict):
    encoded_body = json.dumps(body)
    http = urllib3.PoolManager()
    r = http.request(request_type, address,
                     headers=headers,
                     body=encoded_body)
    return r