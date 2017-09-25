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
    out1, err = util.run_cmd("python3 market_pg_paper_ploat.py ^GSPC 2000-01-01 2017-12-31")
    util.run_cmd("python3 market_pg_train_b.py dow.csv")
    util.run_cmd("python3 market_pg_paper_b.py dow.csv ^DJI")
    out2, err = util.run_cmd("python3 market_pg_paper_ploat.py ^DJI  2000-01-01 2017-12-31")
    print(i, out1, out2)
