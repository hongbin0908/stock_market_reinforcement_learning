import os
import sys
from multiprocessing.pool import ThreadPool

local_path = os.path.dirname(__file__)
root = os.path.join(local_path, '..')
sys.path.append(root)

import util


def train_and_paper(code_list, code):
    pool = ThreadPool(8)
    res = []
    for year in range(2000, 2018):
        for month in range(1, 13):
            ym = "%d-%d" % (year, month)
            train_start, train_end, test_start, test_end = util.train_test_range_month(ym)
            cmd_str = 'python3 market_pg_train.py %s %s %s %s %s 1; ' % (code_list, train_start, train_end, test_start, test_end)
            cmd_str += 'python3 market_pg_paper.py %s %s %s %s %s %s %s' % (code_list, train_start, train_end, code, test_start, test_end, "month")
            e = pool.apply_async(util.run_cmd, (cmd_str,))
            res.append(e)
    for e in res:
        status, out, err = e.get()
        assert 0 == status

for i in range(10000):
    train_and_paper("sp500.csv", "^GSPC")
    status, out1, err = util.run_cmd("python3 market_pg_paper_ploat.py ^GSPC 2000-01-01 2017-12-31 month")
    assert 0 == status
    train_and_paper("dow.csv", "^DJI")
    status, out2, err = util.run_cmd("python3 market_pg_paper_ploat.py ^DJI  2000-01-01 2017-12-31 month")
    assert 0 == status
    print(i, out1, out2)
