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

pids=""

python3 market_pg_train.py sp500.csv 1990-01-01 1999-12-31 2000-01-01 2000-12-31 100 &
python3 market_pg_train.py sp500.csv 1991-01-01 2000-12-31 2001-01-01 2001-12-31 100
wait
python3 market_pg_train.py sp500.csv 1992-01-01 2001-12-31 2002-01-01 2002-12-31 100
python3 market_pg_train.py sp500.csv 1993-01-01 2002-12-31 2003-01-01 2003-12-31 100
python3 market_pg_train.py sp500.csv 1994-01-01 2003-12-31 2004-01-01 2004-12-31 100
python3 market_pg_train.py sp500.csv 1995-01-01 2004-12-31 2005-01-01 2005-12-31 100
python3 market_pg_train.py sp500.csv 1996-01-01 2005-12-31 2006-01-01 2006-12-31 100
python3 market_pg_train.py sp500.csv 1997-01-01 2006-12-31 2007-01-01 2007-12-31 100
python3 market_pg_train.py sp500.csv 1998-01-01 2007-12-31 2008-01-01 2008-12-31 100
python3 market_pg_train.py sp500.csv 1999-01-01 2008-12-31 2009-01-01 2009-12-31 100
python3 market_pg_train.py sp500.csv 2000-01-01 2009-12-31 2010-01-01 2010-12-31 100
python3 market_pg_train.py sp500.csv 2001-01-01 2010-12-31 2011-01-01 2011-12-31 100
python3 market_pg_train.py sp500.csv 2002-01-01 2011-12-31 2012-01-01 2012-12-31 100
python3 market_pg_train.py sp500.csv 2003-01-01 2012-12-31 2013-01-01 2013-12-31 100
python3 market_pg_train.py sp500.csv 2004-01-01 2013-12-31 2014-01-01 2014-12-31 100
python3 market_pg_train.py sp500.csv 2005-01-01 2014-12-31 2015-01-01 2015-12-31 100
python3 market_pg_train.py sp500.csv 2006-01-01 2015-12-31 2016-01-01 2016-12-31 100
python3 market_pg_train.py sp500.csv 2007-01-01 2016-12-31 2017-01-01 2017-12-31 100

popd   > /dev/null # return the directory orignal