import os
import sys
import re
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

local_path = os.path.realpath(os.path.dirname(__file__))
root = os.path.join(local_path, '..')
sys.path.append(root)

def cum_sum(row, signal_name):
    sig = row[signal_name]
    close_rel = row['close_rel']
    if sig == 1:
        cum['cum'] *= close_rel
    elif sig == -1:
        cum['cum'] *= 2-close_rel
    elif sig == 0:
        pass
    else:
        assert False
    return cum['cum']

if __name__ == "__main__":

    argi = 1
    code = sys.argv[argi]; argi += 1
    start = sys.argv[argi]; argi += 1
    end = sys.argv[argi]; argi += 1

    contents = os.walk(local_path)
    dfs = []
    for root, dirs, files in contents:
        for f in files:
            m = re.match(r"paper-.*\.csv", f)
            if m:
                df = pd.read_csv(os.path.join(root, f))
                dfs.append(df)
    df = pd.concat(dfs, axis=0)
    df = df.sort_values('date').reset_index(drop = True)
    cum = {'cum':1}; df['model_cum'] = df.apply(lambda x: cum_sum(x, 'model_signal'), axis=1)
    cum = {'cum':1}; df['bh_cum'] = df.apply(lambda x: cum_sum(x, 'bh_signal'), axis=1)
    cum = {'cum':1}; df['sh_cum'] = df.apply(lambda x: cum_sum(x, 'sh_signal'), axis=1)

    plt.figure(0)
    plt.subplot(121)
    plt.plot(pd.to_datetime(df.date,format='%Y-%m-%d'), df.bh_cum)
    #plt.plot(pd.to_datetime(df.date,format='%Y-%m-%d'), df.sh_cum)
    plt.plot(pd.to_datetime(df.date,format='%Y-%m-%d'), df.model_cum)
    plt.subplot(122)
    plt.plot(pd.to_datetime(df.date,format='%Y-%m-%d'), df.close)
    plt.savefig("paper-%s-%s-%s" % (code, start ,end))
    plt.show()
