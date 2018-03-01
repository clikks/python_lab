#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'lux'

import sys

from pymongo import MongoClient


def get_rank(user_id):
    client = MongoClient()
    db = client.shiyanlou
    contests = db.contests

    group = {'$group': {
                '_id': '$user_id',
                'score': {'$sum': '$score'},
                'submit_time': {'$sum': '$submit_time'}
            }
    }
    sort = {'$sort': {'score': -1, 'submit_time': 1}}
    data = contests.aggregate([group, sort])
    for index, item in enumerate(data):
        if item.get('_id') == user_id:
            rank = index + 1
            score = item.get('score')
            submit_time = item.get('submit_time')
            return rank, score, submit_time
    else:
        print('NOTFOUND')
        sys.exit(1)


if __name__ == '__main__':
    try:
        assert len(sys.argv) == 2
        user_id = int(sys.argv[1])
        userdata = get_rank(user_id)
        print(userdata)
    except Exception as e:
        print("Parameter Error")
