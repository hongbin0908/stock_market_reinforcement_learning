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

python3 market_pg_paper.py sp500.csv 1990-01-01 1999-12-31 ^GSPC 2000-01-01 2000-12-31
python3 market_pg_paper.py sp500.csv 1991-01-01 2000-12-31 ^GSPC 2001-01-01 2001-12-31
python3 market_pg_paper.py sp500.csv 1992-01-01 2001-12-31 ^GSPC 2002-01-01 2002-12-31
python3 market_pg_paper.py sp500.csv 1993-01-01 2002-12-31 ^GSPC 2003-01-01 2003-12-31
python3 market_pg_paper.py sp500.csv 1994-01-01 2003-12-31 ^GSPC 2004-01-01 2004-12-31
python3 market_pg_paper.py sp500.csv 1995-01-01 2004-12-31 ^GSPC 2005-01-01 2005-12-31
python3 market_pg_paper.py sp500.csv 1996-01-01 2005-12-31 ^GSPC 2006-01-01 2006-12-31
python3 market_pg_paper.py sp500.csv 1997-01-01 2006-12-31 ^GSPC 2007-01-01 2007-12-31
python3 market_pg_paper.py sp500.csv 1998-01-01 2007-12-31 ^GSPC 2008-01-01 2008-12-31
python3 market_pg_paper.py sp500.csv 1999-01-01 2008-12-31 ^GSPC 2009-01-01 2009-12-31
python3 market_pg_paper.py sp500.csv 2000-01-01 2009-12-31 ^GSPC 2010-01-01 2010-12-31
python3 market_pg_paper.py sp500.csv 2001-01-01 2010-12-31 ^GSPC 2011-01-01 2011-12-31
python3 market_pg_paper.py sp500.csv 2002-01-01 2011-12-31 ^GSPC 2012-01-01 2012-12-31
python3 market_pg_paper.py sp500.csv 2003-01-01 2012-12-31 ^GSPC 2013-01-01 2013-12-31
python3 market_pg_paper.py sp500.csv 2004-01-01 2013-12-31 ^GSPC 2014-01-01 2014-12-31
python3 market_pg_paper.py sp500.csv 2005-01-01 2014-12-31 ^GSPC 2015-01-01 2015-12-31
python3 market_pg_paper.py sp500.csv 2006-01-01 2015-12-31 ^GSPC 2016-01-01 2016-12-31
python3 market_pg_paper.py sp500.csv 2007-01-01 2016-12-31 ^GSPC 2017-01-01 2017-12-31

popd   > /dev/null # return the directory orignal