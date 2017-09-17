#! /usr/bin/env python3.4
# -*- coding: utf-8 -*-
# @author  Bin Hong

"""
param sym: symbol file
parma start: start ymd
parma end  : end   ymd
"""


import os, sys
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

local_path = os.path.dirname(__file__)
root = os.path.join(local_path, '..')
sys.path.append(root)

def bought_every_day(sym, current_day):
    return 1


cum = 1
def cum_return(sym, row):
    global cum
    position = bought_every_day(sym ,row['date'])
    if 1 == position:
        cum *= row['close_rel']
    elif 0 == position:
        pass
    elif -1 == position:
        pass # no short
    return cum

if __name__ == '__main__':
    """
    symfile = sys.argv[1]
    start = sys.argv[2]
    end = sys.argv[3]
    """

    symfile = os.path.join(local_path, 'data', '^DJI.csv')
    start = '2015-08-26'
    end = '2016-08-25'

    df = pd.read_csv(symfile)
    df = df[(df.date >= start) & (df.date < end)]
    # print df
    dates = pd.to_datetime(df.date, format='%Y-%m-%d')
    #plt.plot(dates, df.close)
    # plt.show()

    df['close_rel']  = (df.close / df.close.shift(1)).fillna(1.0)

    df_cum = df.apply(lambda x: cum_return('^DJI', x), axis = 1)

    plt.plot(dates, df_cum)
    plt.show()