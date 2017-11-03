import quasardb
import datetime as dt
from datetime import timedelta, date
from random import randrange
import json, time, sys

c = quasardb.Cluster('qdb://127.0.0.1:2836')
timeseries = ['ts0', 'ts1']

cluster_uri = 'qdb://127.0.0.1:2836'
separator = '.'
results = []

if cluster_uri != None and separator != None:
    cluster = quasardb.Cluster(cluster_uri)
    tag = cluster.tag('grafana')
    entries = list(tag.get_entries())
    for entry in entries:
        ts = cluster.ts(entry)
        cols = ts.columns_info()
        cols_name = []
        for col in cols:
            name = entry + separator + col.name
            result = {"text": name, "value": name}
            results.append(result)

# insertion of some summy data
for tslabel in timeseries:
    ts = c.ts(tslabel)
    try:
        cols = ts.create([quasardb.TimeSeries.DoubleColumnInfo("col1")])
        ts.attach_tag('grafana')
        col1 = ts.column(quasardb.TimeSeries.DoubleColumnInfo("col1"))
        starttime = dt.datetime.now(quasardb.tz) - timedelta(days=100)
        for i in xrange(0, 1000):
           col1.insert([(starttime + timedelta(minutes=i) , randrange(0, 101, 2))])
    except:
        print 'Something wrong happened : ', sys.exc_info()[0]
        pass
