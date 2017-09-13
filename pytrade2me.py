#! /usr/bin/env python3.4
# -*- coding: utf-8 -*-
# @author  Bin Hong

import os, sys
import pandas as pd


local_path = os.path.dirname(__file__)
root = os.path.join(local_path, '..')
sys.path.append(root)

for line in open(os.path.join(local_path, 'indexes.csv')):
    sym = line.split()[0]
    df = pd.read_csv(os.path.join(local_path, 'index_data', sym + ".csv"))
    print(df.head())
    df.set_index(['date'], drop=True, inplace=True)
    df[['open', 'high', 'low', 'close', 'volume']].to_csv(os.path.join(local_path, 'data', sym + ".csv"))



