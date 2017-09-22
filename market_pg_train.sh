#!/bin/sh
#########################
#@author hongbin0908@126.com
#@date
#@desc TODO
#########################
export PATH=/usr/bin:$PATH
export SCRIPT_PATH=`dirname $(readlink -f $0)` # get the path of the script
pushd . > /dev/null
cd "$SCRIPT_PATH"

python3 market_pg_train.py sp500.csv 1900-01-01 1999-12-31 2000-01-01 2000-12-31 10

popd   > /dev/null # return the directory orignal