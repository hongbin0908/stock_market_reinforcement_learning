import os
import sys
import re
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

local_path = os.path.realpath(os.path.dirname(__file__))
root = os.path.join(local_path, '..')
sys.path.append(root)

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


    plt.plot(pd.to_datetime(df.date,format='%Y-%m-%d'), df.cum_bh)
    plt.savefig("paper-%s-%s-%s" % (code, start ,end))
    plt.show()
