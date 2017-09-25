import os
import sys
from multiprocessing.pool import ThreadPool

local_path = os.path.dirname(__file__)
root = os.path.join(local_path, '..')
sys.path.append(root)

import util

for i in range(10000):
    util.run_cmd("python3 market_pg_train_b.py sp500.csv")
    util.run_cmd("python3 market_pg_paper_b.py sp500.csv ^GSPC")
    out, err = util.run_cmd("python3 market_pg_paper_ploat.py")
    print(i, out)
