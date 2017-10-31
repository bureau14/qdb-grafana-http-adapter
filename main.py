import quasardb
import datetime as dt
from datetime import timedelta, date
import json
import time
from random import randrange

c = quasardb.Cluster('qdb://127.0.0.1:2836')

ts = c.ts("dummy")

cols = ts.create([quasardb.TimeSeries.DoubleColumnInfo("col1"), quasardb.TimeSeries.BlobColumnInfo("col2")])
col1 = ts.column(quasardb.TimeSeries.DoubleColumnInfo("col1"))

for i in xrange(0, 123333):
   col1.insert([(dt.datetime.now(quasardb.tz) - timedelta(days=3) + timedelta(minutes=i) , randrange(0, 101, 2))])
