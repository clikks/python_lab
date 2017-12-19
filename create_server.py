#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import requests


def create_server(name, host):
    # 创建Server
    url = 'http://127.0.0.1:5000/servers/'
    payload = {'name': name, 'host': host}
    headers = {'content-type': 'application/json'}
    r = requests.post(url, data=json.dumps(payload), headers=headers)
    response = r.json()
#    print(response)
    return response


if __name__ == '__main__':
    create_server('redis_test', '127.0.0.1')
