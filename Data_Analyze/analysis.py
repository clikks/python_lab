#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from sys import argv
import json, os.path
import pandas as pd
from pandas import DataFrame

def analysis(file, user_id):
    try:
        user_id = int(user_id)
        if os.path.exists(file):
            with open(file,'r') as f:
                user_data = json.loads(f.read())
            df = DataFrame(user_data)
            user_data = df[df['user_id'] == user_id ]
            times = user_data['created_at'].count()
            minutes = user_data['minutes'].sum()
        else:
            raise ValueError
        return times, minutes
    except:
        return 0


if __name__ == '__main__':
    analysis(argv[1], argv[2])
