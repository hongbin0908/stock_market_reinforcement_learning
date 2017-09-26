import os
import sys
import subprocess

local_path = os.path.dirname(__file__)
root = os.path.join(local_path, '..')
sys.path.append(root)


def run_cmd(cmd_str):
    #print(cmd_str)
    p = subprocess.Popen(cmd_str, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    out, err = p.communicate()
    return (p.returncode, out, err)

DATE_FORMAT = '%Y-%m-%d'

def train_test_range(test_start_year):
    from datetime import datetime
    from datetime import timedelta
    test_start = '%s-01-01' % test_start_year
    test_start_obj = datetime.strptime(test_start, DATE_FORMAT)
    test_end   = '%s-12-31' % test_start_year
    train_end_obj  = test_start_obj - timedelta(days=1)
    train_end = train_end_obj.strftime(DATE_FORMAT)
    train_start_obj = train_end_obj - timedelta(days = 365 * 10)
    train_start = train_start_obj.strftime(DATE_FORMAT)
    return train_start, train_end, test_start ,test_end

def train_test_range_month(test_start_month):
    from datetime import datetime
    from datetime import timedelta
    test_start = '%s-01' % test_start_month
    test_start_obj = datetime.strptime(test_start, DATE_FORMAT)
    test_end_obj = test_start_obj + timedelta(days = 30)
    test_end = test_end_obj.strftime(DATE_FORMAT)
    train_end_obj  = test_start_obj - timedelta(days=1)
    train_end = train_end_obj.strftime(DATE_FORMAT)
    train_start_obj = train_end_obj - timedelta(days = 365)
    train_start = train_start_obj.strftime(DATE_FORMAT)
    return train_start, train_end, test_start ,test_end

def test_range():
    print(train_test_range('2010'))
    print(train_test_range_month('2010-01'))
