#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from cache import RedisCache
import json,redis, time

r = redis.StrictRedis(host='127.0.0.1',db=0)

cache = RedisCache(r)

cache.cache(timeout=10)
def excute(args):
    data = {'name':args,'description':'test data'}
    time.sleep(2)
    print(json.dumps(data))
    return json.dumps(data)



if __name__ == '__main__':
    excute('test')
