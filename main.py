import quasardb
import datetime as dt
from datetime import timedelta, date
import json, time, sys
from random import randrange

c = quasardb.Cluster('qdb://127.0.0.1:2836')
timeseries = ['ts0', 'ts1']

for tslabel in timeseries:
    ts = c.ts(tslabel)
    try:
        cols = ts.create([quasardb.TimeSeries.DoubleColumnInfo("col_grafana")])
        ts.attach_tag('grafana')
        col1 = ts.column(quasardb.TimeSeries.DoubleColumnInfo("col_grafana"))
        starttime = dt.datetime.now(quasardb.tz) - timedelta(days=3)
        for i in xrange(0, 1000):
           col1.insert([(starttime + timedelta(minutes=i) , randrange(0, 101, 2))])
    except:
        print 'Something wrong happened : ', sys.exc_info()[0]
        pass
