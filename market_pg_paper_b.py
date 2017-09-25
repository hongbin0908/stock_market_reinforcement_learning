import os
import sys
import subprocess
import multiprocessing
from multiprocessing.pool import ThreadPool
import shlex

local_path = os.path.dirname(__file__)
root = os.path.join(local_path, '..')
sys.path.append(root)



def run_cmd(cmd_str):
    p = subprocess.Popen(cmd_str, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    out, err = p.communicate()
    return (out, err)

pool = ThreadPool(4)
for year in range(2000, 2018):
    from datetime import datetime
    from datetime import timedelta
    test_start = '%s-01-01' % year
    test_start_obj = datetime.strptime(test_start, '%Y-%m-%d')
    test_end   = '%s-12-31' % year
    train_end_obj  = test_start_obj - timedelta(days=1)
    train_end = train_end_obj.strftime('%Y-%m-%d')
    train_start_obj = train_end_obj - timedelta(years = 10)
    train_start = train_start_obj.strftime('%Y-%m-%d')
    cmd_str = 'python3 market_pg_paper.py sp500.csv %s %s ^GSPC %s %s' % (train_start, train_end, test_start, test_end)
    print(cmd_str)
    pool.apply_async(run_cmd, cmd_str)


#python3 market_pg_paper.py sp500.csv 1990-01-01 1999-12-31 ^GSPC 2000-01-01 2000-12-31
#python3 market_pg_paper.py sp500.csv 1991-01-01 2000-12-31 ^GSPC 2001-01-01 2001-12-31
#python3 market_pg_paper.py sp500.csv 1992-01-01 2001-12-31 ^GSPC 2002-01-01 2002-12-31
#python3 market_pg_paper.py sp500.csv 1993-01-01 2002-12-31 ^GSPC 2003-01-01 2003-12-31
#python3 market_pg_paper.py sp500.csv 1994-01-01 2003-12-31 ^GSPC 2004-01-01 2004-12-31
#python3 market_pg_paper.py sp500.csv 1995-01-01 2004-12-31 ^GSPC 2005-01-01 2005-12-31
#python3 market_pg_paper.py sp500.csv 1996-01-01 2005-12-31 ^GSPC 2006-01-01 2006-12-31
#python3 market_pg_paper.py sp500.csv 1997-01-01 2006-12-31 ^GSPC 2007-01-01 2007-12-31
#python3 market_pg_paper.py sp500.csv 1998-01-01 2007-12-31 ^GSPC 2008-01-01 2008-12-31
#python3 market_pg_paper.py sp500.csv 1999-01-01 2008-12-31 ^GSPC 2009-01-01 2009-12-31
#python3 market_pg_paper.py sp500.csv 2000-01-01 2009-12-31 ^GSPC 2010-01-01 2010-12-31
#python3 market_pg_paper.py sp500.csv 2001-01-01 2010-12-31 ^GSPC 2011-01-01 2011-12-31
#python3 market_pg_paper.py sp500.csv 2002-01-01 2011-12-31 ^GSPC 2012-01-01 2012-12-31
#python3 market_pg_paper.py sp500.csv 2003-01-01 2012-12-31 ^GSPC 2013-01-01 2013-12-31
#python3 market_pg_paper.py sp500.csv 2004-01-01 2013-12-31 ^GSPC 2014-01-01 2014-12-31
#python3 market_pg_paper.py sp500.csv 2005-01-01 2014-12-31 ^GSPC 2015-01-01 2015-12-31
#python3 market_pg_paper.py sp500.csv 2006-01-01 2015-12-31 ^GSPC 2016-01-01 2016-12-31
#python3 market_pg_paper.py sp500.csv 2007-01-01 2016-12-31 ^GSPC 2017-01-01 2017-12-31
