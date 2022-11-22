import pymongo as pm
import datetime
import time
import matplotlib.pyplot as plt
import numpy as np
import sys
import json
import os
import pandas as pd
from utils import *



def all_sensor_analysis(db_info, sensor_names, start_ts, end_ts):
    ''' Data Crawling from Lapras DB '''
    client = pm.MongoClient(db_info['address'])
    client.data.authenticate(db_info['autheticate']['name'], db_info['autheticate']['pw'], mechanism=db_info['autheticate']['mechanism'])
    db = client.data
    data = db.N1SeminarRoom825_data

    sensor_values = [(d['timestamp'], d['name'], d['value'], d['publisher']) for d in \
        data.find({'timestamp': {'$gt': start_ts, '$lt': end_ts}, 'type': 'context', 'publisher': {'$in': sensor_names}}).sort('timestamp')]

    client.close()

    # print(sensor_values[1])
    np_datas = np.array(sensor_values)
    pivot = pd.DataFrame(np_datas, columns=['timestamp', 'name', 'value', 'publisher'])
    fname = 'sensor_datas.csv'

    pivot.to_csv(fname, sep=',', na_rep='NaN')

def query_context(db_info, cname, context_names, start_ts, end_ts):
    ''' Data Crawling from Lapras DB '''
    client = pm.MongoClient(db_info['address'])
    client.data.authenticate(db_info['autheticate']['name'], db_info['autheticate']['pw'], mechanism=db_info['autheticate']['mechanism'])
    db = client.data
    data = db.N1SeminarRoom825_data

    sensor_values = [(d['timestamp'], d['name'], d['value'], d['publisher']) for d in \
        data.find({'timestamp': {'$gt': start_ts, '$lt': end_ts}, 'type': 'context', 'name': {'$in': context_names}}).sort('timestamp')]

    client.close()

    np_datas = np.array(sensor_values)
    pivot = pd.DataFrame(np_datas, columns=['timestamp', 'name', 'value', 'publisher'])
    fname = f'query/{cname}.csv'

    pivot.to_csv(fname, sep=',', na_rep='NaN')

def query_action(db_info, aname, action_names, start_ts, end_ts):
    ''' Data Crawling from Lapras DB '''
    client = pm.MongoClient(db_info['address'])
    client.data.authenticate(db_info['autheticate']['name'], db_info['autheticate']['pw'], mechanism=db_info['autheticate']['mechanism'])
    db = client.data
    data = db.N1SeminarRoom825_data

    sensor_values = [(d['timestamp'], d['name'], d['publisher']) for d in \
        data.find({'timestamp': {'$gt': start_ts, '$lt': end_ts}, 'type': 'action', 'name': {'$in': action_names}}).sort('timestamp')]

    client.close()

    np_datas = np.array(sensor_values)
    pivot = pd.DataFrame(np_datas, columns=['timestamp', 'name', 'publisher'])
    fname = f'query/{aname}.csv'

    pivot.to_csv(fname, sep=',', na_rep='NaN')

if __name__ == '__main__':
    start_ts = int(time.mktime(datetime.datetime(2017, 1, 1, 0, 0).timetuple())*1000)
    end_ts = int(time.mktime(datetime.datetime(2018, 1, 1, 0, 0).timetuple())*1000)

    json_file = 'db_info.json'
    with open(json_file, 'r') as f:
        db_info = json.load(f)
    

    context_files = os.listdir('context_lists')
    context_files = list(filter(lambda x: '.txt' in x, context_files))
    for fname in context_files:
        name = fname.split('.')[0]
        names = load_list(f'context_lists/{fname}')
        print(name)
        query_context(db_info, name, names, start_ts, end_ts)
        # query_action(db_info, name, names, start_ts, end_ts)

        