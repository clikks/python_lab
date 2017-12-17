#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
from functools import wraps

class RedisCache:
    # 缓存系统类

    def __init__(self, redis_client):
        self._redis = redis_client

    def cache(self, timeout=0):
        self._timeout = timeout
        # Aargs: time(int): 缓存时间
        def derecotor(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                # self_args = *args
                # self_kwargs = **kwargs
                func_info = (self.func.__name__,args,kwargs)
                print(func_info)
                if self._redis.exists(func_info) and timeout != 0:
                    result = self._redis.get(func_info)
                    return json.dumps(result)
                else:
                    new = self.func(*args,**kwargs)
                    result = json.loads(new)
                    new_func_info = (self.func.__name__, args, kwargs)
                    print(new_func_info)
                    self._redis.set(new_func_info, result, ex=self_timeout)
                    return new
            return wrapper
        return derecotor