import os
import sys
import time
import json
import datetime
import pymongo as pm
import pandas as pd
import numpy as np
from utils import *



def one_task_analysis(db_info, task_name, start_ts, end_ts):
    ''' Data Crawling from Lapras DB '''
    client = pm.MongoClient(db_info['address'])
    client.data.authenticate(db_info['autheticate']['name'], db_info['autheticate']['pw'], mechanism=db_info['autheticate']['mechanism'])
    db = client.data
    data = db.N1SeminarRoom825_Annotation

    sensor_values = [d['start_timestamp'] for d in \
        data.find({'start_timestamp': {'$gt': start_ts, '$lt': end_ts}, 'label': task_name}).sort('timestamp')]

    client.close()

    ''' Process the timestamp & value data '''
    scale = 1000*60*60*24
    ts = list(map(lambda x: to_day(x), sensor_values))
    np_ts_to_dt = np.vectorize(ts_to_dt)

    all_ts_data = np.array(list(range(start_ts, end_ts+1, scale)))
    all_ts_data = np_ts_to_dt(all_ts_data)
    all_task_data = np.zeros_like(all_ts_data, dtype=np.int)

    for i in range(len(sensor_values)):
        all_task_data[(ts[i]-start_ts)//scale] += 1

    return all_ts_data, all_task_data

def multi_task_analysis(db_info, task_list, start_ts, end_ts):
    scale = 1000*60*60*24
    np_ts_to_dt = np.vectorize(ts_to_dt)
    all_ts_data = np.array(list(range(start_ts, end_ts+1, scale)))
    all_ts_data = np_ts_to_dt(all_ts_data)

    all_task_datas = np.zeros((len(task_list), len(all_ts_data)), dtype=np.float32)
    
    for i, sensor_name in enumerate(task_list):
        print(f'[{i}] {sensor_name}')
        _, all_task_data = one_task_analysis(db_info, sensor_name, start_ts, end_ts)
        all_task_datas[i] = all_task_data

    start_dt = ts_to_dt(start_ts)
    end_dt = ts_to_dt(end_ts)
    fname = start_dt.replace('/', '')+'-'+end_dt.replace('/', '')+'_task.xlsx'


    pivot = pd.DataFrame(all_task_datas, index=task_list, columns=all_ts_data)
    pivot.to_excel(fname,
                    sheet_name='Sheet1',
                    na_rep = 'NaN', 
                    float_format = "%.3f", 
                    header = True, 
                    index = True, 
                    index_label = "task", 
            ) 

if __name__ == '__main__':
    start_ts = int(time.mktime(datetime.datetime(2017, 9, 1, 0, 0).timetuple())*1000)
    end_ts = int(time.mktime(datetime.datetime(2018, 1, 1, 0, 0).timetuple())*1000)

    json_file = 'db_info.json'
    with open(json_file, 'r') as f:
        db_info = json.load(f)

    task_list = load_list('task_list.txt')
    print(task_list)
    multi_task_analysis(db_info, task_list, start_ts, end_ts)