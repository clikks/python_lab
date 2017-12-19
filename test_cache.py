#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import redis
from cache import RedisCache

r = redis.StrictRedis(host='127.0.0.1', db=0)
cache = RedisCache(r)


@cache.cache(timeout=10)
def excute(args):
    data = {'name': args, 'description': 'test data'}
    # print(json.dumps(data))
    return data


if __name__ == '__main__':
    excute('test')
