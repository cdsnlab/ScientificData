import os
import sys
import time
import json
import datetime
import pymongo as pm
import pandas as pd
import numpy as np

def ts_to_dt(timestamp):
    return datetime.datetime.fromtimestamp(timestamp/1000).strftime('%y.%m.%d.%H:%M:%S')

def query_sensor_activity(db_info, pair_path, flag=False, video_name=False, dt=False, matched=False, empty=False, only_meta=False):
    ''' Connect DB '''
    client = pm.MongoClient(db_info['address'])
    client.data.authenticate(db_info['autheticate']['name'], db_info['autheticate']['pw'], mechanism=db_info['autheticate']['mechanism'])
    db = client.data
    annotation_data = db.N1SeminarRoom825_Annotation
    sensor_data = db.N1SeminarRoom825_data

    options = {'date': { '$regex' : "2017", '$options' : 'i' }}
    selects = ['start_timestamp', 'end_timestamp', 'label', 'avg_n_human']

    pair_df = pd.read_excel(pair_path, sheet_name=None)

    env_contexts = list(pair_df['env']['name'])
    env_sensors = list(pair_df['env']['sensor_name'])
    new_env_name = dict(zip(env_contexts, env_sensors))

    act_contexts = list(pair_df['act']['name'])
    act_sensors = list(pair_df['act']['sensor_name'])
    new_act_name = dict(zip(act_contexts, act_sensors))

    sound_contexts = list(pair_df['sound']['name'])
    sound_sensors = list(pair_df['sound']['sensor_name'])
    new_sound_name = dict(zip(sound_contexts, sound_sensors))


    if flag:
        options['flag'] = True
    if matched:
        options['matched'] = True
    if video_name:
        selects.append('video_names')
    
    result_df_columns = ['label', 'start_ts', 'end_ts', 'avg_n_human', 'duration']
    if video_name:
        result_df_columns.append('video_names')
    if dt:
        result_df_columns.append('start_dt')
        result_df_columns.append('end_dt')
    result_df = pd.DataFrame(columns=result_df_columns)

    ''' Query Activity list '''
    activities = [tuple(map(lambda x: d[x], selects)) for d in \
        annotation_data.find(options).sort('date').sort('start_timestamp')]

    for activity in activities:
        start_ts, end_ts, label, avg_n_human = activity[0], activity[1], activity[2], activity[3]
        if video_name:
            video_names = activity[4]
        
        ''' Wrong label check '''
        if label in ['?', '---', '-']:
            continue


        ''' Query context and action data'''
        # ambient, monnit, light, aircon, projector
        contexts = [[d['timestamp'], new_env_name[d['name']], d['value']] for d in \
            sensor_data.find({'name': {'$in': env_contexts}, 'timestamp': {'$gt': start_ts, '$lt': end_ts}, 'type': 'context'}).sort('timestamp')]

        # only for dooragent
        actions = [[d['timestamp'], new_act_name[d['name']], 'activate'] for d in \
            sensor_data.find({'name': {'$in': act_contexts}, 'timestamp': {'$gt': start_ts, '$lt': end_ts}, 'type': 'action'}).sort('timestamp')]

        # sound
        sounds = [[d['timestamp'], new_sound_name[d['name']], d['value']] for d in \
            sensor_data.find({'name': {'$in': sound_contexts}, 'timestamp': {'$gt': start_ts, '$lt': end_ts}, 'type': 'context'}).sort('timestamp')]

        ''' Wrong brightness value handling '''
        contexts = list(filter(lambda x: not (x[1] in ['Brightness_1', 'Brightness_2'] and x[2] < 2), contexts))
        
        sound_table = {'Sound_L': [], 'Sound_R': [], 'Sound_C': []}
        stack_table = {'Sound_L': [], 'Sound_R': [], 'Sound_C': []}
        last_ts_table = {'Sound_L': 0, 'Sound_R': 0, 'Sound_C': 0}

        for i, sdata in enumerate(sounds):
            sound_name = sdata[1]
            if sdata[0] - last_ts_table[sound_name] > 5000:
                if len(stack_table[sound_name]) > 0:
                    sound_table[sound_name].append([stack_table[sound_name][0][0], sound_name, sum(list(map(lambda x: x[2], stack_table[sound_name])))/len(stack_table[sound_name])])
                    stack_table[sound_name].clear()
            stack_table[sound_name].append(sdata)
            last_ts_table[sound_name] = sdata[0]


        ''' Data Processing '''
        sensor_values = sorted(contexts + actions + sound_table['Sound_L'] + sound_table['Sound_R'] + sound_table['Sound_C'], key=lambda x: x[0])        
        columns= ['timestamp', 'sensor_name', 'value']

        ''' List empty check '''
        if not sensor_values:
            if empty:
                continue
            print(f'{label}_{start_ts}')
            sensor_values = [['', '', '']]
            
        if dt:
            columns.append('datetime')
            if sensor_values[0][0] != '':
                sensor_values = list(map(lambda x: x + [ts_to_dt(x[0])], sensor_values))
            else:
                sensor_values[0].append('')

        sensor_table = pd.DataFrame(np.array(sensor_values), columns=columns)


        metadata_header = result_df_columns
        metadata_content = [f'{label}', f'{start_ts}', f'{end_ts}', f'{avg_n_human}', f'{(end_ts-start_ts)//1000}']
        if video_name:
            metadata_content.append(f'{video_names}')
        if dt:
            metadata_content.append(f'{ts_to_dt(start_ts)}')
            metadata_content.append(f'{ts_to_dt(end_ts)}')
        
        result_df = result_df.append(pd.DataFrame([metadata_content], columns=metadata_header), ignore_index=True)

        ''' Setup to save result files '''
        sensor_dir = 'sensor'
        metadata_dir = 'metadata'
        if not os.path.isdir(sensor_dir):
            os.mkdir(sensor_dir)
        if not os.path.isdir(metadata_dir):
            os.mkdir(metadata_dir)

        sensor_fname = f'{sensor_dir}/{label}_{start_ts}.csv'
        metadata_fname = f'{metadata_dir}/{label}_{start_ts}.txt'

        ''' Save Sensor data'''
        if not only_meta:
            sensor_table.to_csv(sensor_fname, sep=',', na_rep='', index=False)

        ''' Save Meta data '''
        with open(metadata_fname, 'w') as f:
            for i in range(len(metadata_header)):
                f.write(f'{metadata_header[i]}: {metadata_content[i]}\n')
            f.close()
    

    ''' Save summary file '''
    result_df.to_excel('SensorData_summary.xlsx', index=False)
    client.close()

    

if __name__ == '__main__':
    json_file = 'info/db_info.json'
    with open(json_file, 'r') as f:
        db_info = json.load(f)
        f.close()

    pair_path = 'info/context_name_map.xlsx'

    flag = False
    video_name = False
    dt = False
    matched = False
    monnit = False
    empty = False
    only_meta = False
    
    query_sensor_activity(db_info, pair_path, flag, video_name, dt, matched, empty, only_meta)