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
            

# for i in results:
#     if i.get('value', None) != None:
#         print i.get('value').split(separator)[0]
#         print i.get('value').split(separator)[1]

# for tslabel in timeseries:
#     ts = c.ts(tslabel)
#     try:
#         cols = ts.create([quasardb.TimeSeries.DoubleColumnInfo("col_grafana")])
#         ts.attach_tag('grafana')
#         col1 = ts.column(quasardb.TimeSeries.DoubleColumnInfo("col_grafana"))
#         starttime = dt.datetime.now(quasardb.tz) - timedelta(days=100)
#         for i in xrange(0, 1000):
#            col1.insert([(starttime + timedelta(minutes=i) , randrange(0, 101, 2))])
#     except:
#         print 'Something wrong happened : ', sys.exc_info()[0]
#         pass
