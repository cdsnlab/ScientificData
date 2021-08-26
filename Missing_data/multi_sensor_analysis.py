import sys
import time
import json
import datetime
import numpy as np
import pandas as pd
from utils import *
from one_sensor_analysis import one_context_analysis, one_sensor_analysis

def multi_context_analysis(db_info, context_list, start_ts, end_ts):
    scale = 1000*60*60*24
    np_ts_to_dt = np.vectorize(ts_to_dt)
    all_ts_data = np.array(list(range(start_ts, end_ts+1, scale)))
    all_ts_data = np_ts_to_dt(all_ts_data)

    all_context_datas = np.zeros((len(context_list), len(all_ts_data)), dtype=np.float32)
    
    for i, sensor_name in enumerate(context_list):
        print(f'[{i}] {sensor_name}')
        _, all_context_data = one_context_analysis(db_info, sensor_name, start_ts, end_ts)
        all_context_datas[i] = all_context_data

    start_dt = ts_to_dt(start_ts)
    end_dt = ts_to_dt(end_ts)
    fname = start_dt.replace('/', '')+'-'+end_dt.replace('/', '')+'_context.xlsx'


    pivot = pd.DataFrame(all_context_datas, index=context_list, columns=all_ts_data)
    pivot.to_excel(fname,
                    sheet_name='Sheet1',
                    na_rep = 'NaN', 
                    float_format = "%.3f", 
                    header = True, 
                    index = True, 
                    index_label = "context", 
            ) 

def multi_sensor_analysis(db_info, sensor_list, start_ts, end_ts):
    scale = 1000*60*60*24
    np_ts_to_dt = np.vectorize(ts_to_dt)
    all_ts_data = np.array(list(range(start_ts, end_ts+1, scale)))
    all_ts_data = np_ts_to_dt(all_ts_data)

    all_sensor_datas = np.zeros((len(sensor_list), len(all_ts_data)), dtype=np.float32)
    
    for i, sensor_name in enumerate(sensor_list):
        print(f'[{i}] {sensor_name}')
        _, all_sensor_data = one_sensor_analysis(db_info, sensor_name, start_ts, end_ts)
        all_sensor_datas[i] = all_sensor_data

    start_dt = ts_to_dt(start_ts)
    end_dt = ts_to_dt(end_ts)
    fname = start_dt.replace('/', '')+'-'+end_dt.replace('/', '')+'_sensor.xlsx'


    pivot = pd.DataFrame(all_sensor_datas, index=sensor_list, columns=all_ts_data)
    pivot.to_excel(fname,
                    sheet_name='Sheet1',
                    na_rep = 'NaN', 
                    float_format = "%.3f", 
                    header = True, 
                    index = True, 
                    index_label = "sensor", 
            ) 


if __name__ == '__main__':
    start_ts = int(time.mktime(datetime.datetime(2017, 9, 1, 0, 0).timetuple())*1000)
    end_ts = int(time.mktime(datetime.datetime(2018, 1, 1, 0, 0).timetuple())*1000)

    json_file = 'db_info.json'
    with open(json_file, 'r') as f:
        db_info = json.load(f)

    # sensor_list = load_sensor_list()
    # sensor_list = load_list('agent_list.txt')
    # print(sensor_list)
    # multi_sensor_analysis(db_info, sensor_list, start_ts, end_ts)

    # context_list = load_context_list()
    context_list = load_list('context_lists/1709to12_context.txt')
    print(context_list)
    multi_context_analysis(db_info, context_list, start_ts, end_ts)

    
    