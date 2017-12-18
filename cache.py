#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json, base64, pickle
from functools import wraps

class RedisCache:

    def __init__(self, redis_client):
        self._redis = redis_client

    def cache(self, timeout=0):
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                data = pickle.dumps((func.__name__,args))
                key = base64.b64encode(data)

                if timeout == 0:
                    return func(*args, **kwargs)
                result = self._redis.get(key)
                if result:
                    result = str(result,encoding='utf-8')
                    # print(result)
                    # result = eval(result)
                    result = json.loads(result)
                    # print(result,type(result))
                    return result
                else:
                    new = func(*args,**kwargs)
                    value = json.dumps(new)
                    # key = func.__name__
                    self._redis.set(key, value, ex=timeout)
                    return new
            return wrapper
        return decorator
