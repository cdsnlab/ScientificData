import pymongo as pm
import datetime
import time
import matplotlib.pyplot as plt
import numpy as np
import sys
import json
import pandas as pd
from utils import *


def one_context_analysis(db_info, context_name, start_ts, end_ts):
    ''' Data Crawling from Lapras DB '''
    client = pm.MongoClient(db_info['address'])
    client.data.authenticate(db_info['autheticate']['name'], db_info['autheticate']['pw'], mechanism=db_info['autheticate']['mechanism'])
    db = client.data
    data = db.N1SeminarRoom825_data

    sensor_values = [d['timestamp'] for d in \
        data.find({'timestamp': {'$gt': start_ts, '$lt': end_ts}, 'name': context_name}).sort('timestamp')]

    client.close()

    ''' Process the timestamp & value data '''
    scale = 1000*60*60*24
    ts = list(map(lambda x: to_day(x), sensor_values))
    np_ts_to_dt = np.vectorize(ts_to_dt)

    all_ts_data = np.array(list(range(start_ts, end_ts+1, scale)))
    all_ts_data = np_ts_to_dt(all_ts_data)
    all_sensor_data = np.zeros_like(all_ts_data, dtype=np.int)

    for i in range(len(sensor_values)):
        all_sensor_data[(ts[i]-start_ts)//scale] += 1

    return all_ts_data, all_sensor_data

def one_context_value_analysis(db_info, context_name, start_ts, end_ts):
    ''' Data Crawling from Lapras DB '''
    client = pm.MongoClient(db_info['address'])
    client.data.authenticate(db_info['autheticate']['name'], db_info['autheticate']['pw'], mechanism=db_info['autheticate']['mechanism'])
    db = client.data
    data = db.N1SeminarRoom825_data

    sensor_values = [(d['timestamp'], d['value']) for d in \
        data.find({'timestamp': {'$gt': start_ts, '$lt': end_ts}, 'name': context_name}).sort('timestamp')]

    client.close()

    ''' Process the timestamp & value data '''
    np_datas = np.array(sensor_values)
    pivot = pd.DataFrame(np_datas, columns=['timestamp', 'value'])
    fname = f'context/{context_name}.csv'

    pivot.to_csv(fname, sep=',', na_rep='NaN')

    # for i in range(len(sensor_values)):
    #     all_sensor_data[(ts[i]-start_ts)//scale] += 1
    # ts = list(map(lambda x: x[0], sensor_values))
    # values = list(map(lambda x: x[1], sensor_values))
    # plt.plot(ts, values, label=context_name)
    # plt.savefig(f'context/{context_name}.png')
    # plt.clf()

def one_sensor_analysis(db_info, sensor_name, start_ts, end_ts):
    ''' Data Crawling from Lapras DB '''
    client = pm.MongoClient(db_info['address'])
    client.data.authenticate(db_info['autheticate']['name'], db_info['autheticate']['pw'], mechanism=db_info['autheticate']['mechanism'])
    db = client.data
    data = db.N1SeminarRoom825_data

    sensor_values = [d['timestamp'] for d in \
        data.find({'timestamp': {'$gt': start_ts, '$lt': end_ts}, 'publisher': sensor_name}).sort('timestamp')]

    client.close()

    ''' Process the timestamp & value data '''
    scale = 1000*60*60*24
    ts = list(map(lambda x: to_day(x), sensor_values))
    np_ts_to_dt = np.vectorize(ts_to_dt)

    all_ts_data = np.array(list(range(start_ts, end_ts+1, scale)))
    all_ts_data = np_ts_to_dt(all_ts_data)
    all_sensor_data = np.zeros_like(all_ts_data, dtype=np.int)

    for i in range(len(sensor_values)):
        all_sensor_data[(ts[i]-start_ts)//scale] += 1

    return all_ts_data, all_sensor_data

if __name__ == '__main__':
    start_ts = int(time.mktime(datetime.datetime(2017, 1, 1, 0, 0).timetuple())*1000)
    end_ts = int(time.mktime(datetime.datetime(2018, 1, 1, 0, 0).timetuple())*1000)

    json_file = 'db_info.json'
    with open(json_file, 'r') as f:
        db_info = json.load(f)

    context_list = load_list('sound_context.txt')

    print(context_list)

    for context_name in context_list:
        print(context_name)
        one_context_value_analysis(db_info, context_name, start_ts, end_ts)
    # plt.legend()
    # plt.savefig(f'context/sound.png')
    # plt.clf()


        