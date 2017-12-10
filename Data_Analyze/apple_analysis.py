#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
from pandas import Series, DataFrame
import os.path

def quarter_volume(filepath):
    if os.path.exists(filepath):
        data = pd.read_csv(filepath, header=0, index_col=0, parse_dates=True)
        quarter_data = data.resample('Q').sum()
        second_volume = quarter_data.sort_values(by='Volume', ascending=False).head(2).tail(1).Volume.tolist()[0]
    return int(second_volume)


if __name__ == '__main__':
    filepath = '/home/shiyanlou/Code/apple.csv'
    #second_volume = quarter_volume(filepath)
    #print(second_volume,type(second_volume))
    quarter_volume(filepath)
