import os
import sys
from multiprocessing.pool import ThreadPool

local_path = os.path.dirname(__file__)
root = os.path.join(local_path, '..')
sys.path.append(root)

import util

argi = 1
codeListFilename = sys.argv[argi]; argi +=1
pool = ThreadPool(8)
res = []
for year in range(2000, 2018):
    from datetime import datetime
    from datetime import timedelta
    test_start = '%s-01-01' % year
    test_start_obj = datetime.strptime(test_start, '%Y-%m-%d')
    test_end   = '%s-12-31' % year
    train_end_obj  = test_start_obj - timedelta(days=1)
    train_end = train_end_obj.strftime('%Y-%m-%d')
    train_start_obj = train_end_obj - timedelta(days = 365)
    train_start = train_start_obj.strftime('%Y-%m-%d')
    cmd_str = 'python3 market_pg_train.py %s %s %s %s %s 100' % (codeListFilename, train_start, train_end, test_start, test_end)
    e = pool.apply_async(util.run_cmd, (cmd_str,))
    res.append(e)
for e in res:
    print(e.get())
