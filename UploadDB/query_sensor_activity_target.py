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

def context_correction(timestamp, context_name):
    sound_correction = {'SoundEntrance1': 'SoundCenter0', 'SoundEntrance2': 'SoundCenter1', 'SoundEntrance3': 'SoundCenter2', 
                        'SoundWall1': 'SoundWall0', 'SoundWall2': 'SoundWall1', 'SoundWall3': 'SoundWall2', 
                        'SoundWindow1': 'SoundWindow0', 'SoundWindow2': 'SoundWindow1', 'SoundWindow3': 'SoundWindow2'}
    corrected_context = context_name
    if timestamp < 1511967600000: # 2017.11.30
        if context_name in sound_correction.keys():
            corrected_context = sound_correction[context_name]
    
    return corrected_context


def query_sensor_activity(db_info, pair_path, flag=False, video_name=False, dt=False, matched=False, monnit=False, sound=False, empty=False):
    ''' Connect DB '''
    client = pm.MongoClient(db_info['address'])
    client.data.authenticate(db_info['autheticate']['name'], db_info['autheticate']['pw'], mechanism=db_info['autheticate']['mechanism'])
    db = client.data
    annotation_data = db.N1SeminarRoom825_Annotation
    sensor_data = db.N1SeminarRoom825_data

    options = {'date': { '$regex' : "2017", '$options' : 'i' }}
    selects = ['start_timestamp', 'end_timestamp', 'label', 'avg_n_human']

    pair_df = pd.read_excel(pair_path)
    context_names = list(pair_df['name'])
    publisher_names = list(pair_df['publisher'])

    context_to_publisher = dict(zip(context_names, publisher_names))

    if flag:
        options['flag'] = True
    if matched:
        options['matched'] = True
    if video_name:
        selects.append('video_names')
    
    result_df_columns = ['label', 'start_ts', 'end_ts', 'avg_n_human']
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
        contexts = [[d['timestamp'], context_to_publisher[context_correction(d['timestamp'], d['name'])], context_correction(d['timestamp'], d['name']), d['value']] for d in \
            sensor_data.find({'name': {'$in': context_names}, 'timestamp': {'$gt': start_ts, '$lt': end_ts}, 'type': 'context'}).sort('timestamp')]
        actions = [[d['timestamp'], context_to_publisher[d['name']], d['name'], None] for d in \
            sensor_data.find({'name': {'$in': context_names}, 'timestamp': {'$gt': start_ts, '$lt': end_ts}, 'type': 'action'}).sort('timestamp')]

        ''' Wrong brightness value handling '''
        contexts = list(filter(lambda x: not (x[2] in ['sensor0_Brightness', 'sensor1_Brightness'] and x[3] < 2), contexts))
        
        ''' Data Processing '''
        sensor_values = sorted(contexts + actions, key=lambda x: x[0])        
        columns= ['timestamp', 'publisher', 'name', 'value']
        

        ''' List empty check '''
        if not sensor_values:
            if empty:
                continue
            print(f'{label}_{start_ts}')
            sensor_values = [['', '', '', '']]
            
        if dt:
            columns.append('datetime')
            if sensor_values[0][0] != '':
                sensor_values = list(map(lambda x: x + [ts_to_dt(x[0])], sensor_values))
            else:
                sensor_values[0].append('')

        sensor_table = pd.DataFrame(np.array(sensor_values), columns=columns)

        ''' Monnit agent check '''
        if monnit: 
            if not 'MonnitServerAgent' in list(sensor_table['publisher']):
                continue
        if sound:
            if not 'SoundSensorAgent' in list(sensor_table['publisher']):
                continue

        metadata_header = result_df_columns
        metadata_content = [f'{label}', f'{start_ts}', f'{end_ts}', f'{avg_n_human}']
        if video_name:
            metadata_content.append(f'{video_names}')
        if dt:
            metadata_content.append(f'{ts_to_dt(start_ts)}')
            metadata_content.append(f'{ts_to_dt(end_ts)}')
        
        # print(metadata_header, metadata_content)
        result_df = result_df.append(pd.DataFrame([metadata_content], columns=metadata_header), ignore_index=True)

        ''' Save each activity data '''
        sensor_dir = 'sensor'
        metadata_dir = 'metadata'
        if not os.path.isdir(sensor_dir):
            os.mkdir(sensor_dir)
        if not os.path.isdir(metadata_dir):
            os.mkdir(metadata_dir)

        sensor_fname = f'{sensor_dir}/{label}_{start_ts}.csv'
        metadata_fname = f'{metadata_dir}/{label}_{start_ts}.txt'
        sensor_table.to_csv(sensor_fname, sep=',', na_rep='')
        with open(metadata_fname, 'w') as f:
            for i in range(len(metadata_header)):
                f.write(f'{metadata_header[i]}: {metadata_content[i]}\n')
            f.close()
    
    result_df.to_excel('SensorData_summary.xlsx')
    client.close()

    

if __name__ == '__main__':
    json_file = 'info/db_info.json'
    with open(json_file, 'r') as f:
        db_info = json.load(f)
        f.close()

    pair_path = 'info/pair_17_9to12.xlsx'

    flag = False
    video_name = True
    dt = True
    matched = False
    monnit = False
    sound = False
    empty = False
    
    query_sensor_activity(db_info, pair_path, flag, video_name, dt, matched, monnit, sound, empty)