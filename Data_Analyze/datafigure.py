#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pandas import DataFrame

def Datafig(filepath):
    data = pd.read_json(filepath)
    result = data[['user_id','minutes']].groupby('user_id').sum()
    
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    ax.set_title("StudyData")
    
    xmajor_ticks = np.arange(result.index.min(), result.index.max(), 40000)
    xminor_ticks = np.arange(result.index.min(), result.index.max(), 20000)
    #ymajor_ticks = np.arange(result['minutes'].min(), result['minutes'].max()+1, 100)
    #yminor_ticks = np.arange(result['minutes'].min(), result['minutes'].max()+1, 50)

    ax.set_xticks(xmajor_ticks)
    ax.set_xticks(xminor_ticks, minor=True)
    #ax.set_yticks(ymajor_ticks)
    #ax.set_yticks(yminor_ticks, minor=True)

    ax.set_xlabel("User ID")
    ax.set_ylabel("Study Time")

    ax.grid(which='minor', alpha=0.2)
    ax.grid(which='major', alpha=0.5)
    x = result.index
    y = result['minutes']
    ax.plot(x, y)
    fig.show()

if __name__ == '__main__':
    filepath = '/home/shiyanlou/Code/user_study.json'
    Datafig(filepath)
    input()
