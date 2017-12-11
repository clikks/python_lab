#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
from pandas import Series, DataFrame

def quarter_volume():
    data = pd.read_csv('apple.csv', header=0, index_col=0, parse_dates=True)
    quarter_data = data.resample('Q').sum().sort_values(by='Volume', ascending=False)
    second_volume = quarter_data.head(2).tail(1).Volume.tolist()[0]
    return second_volume


