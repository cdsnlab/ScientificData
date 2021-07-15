import os
import time
import json
import datetime
import pymongo as pm
import pandas as pd
import numpy as np

def query_sensor_activity(db_info):
    ''' Connect DB '''
    client = pm.MongoClient(db_info['address'])
    client.data.authenticate(db_info['autheticate']['name'], db_info['autheticate']['pw'], mechanism=db_info['autheticate']['mechanism'])
    db = client.data
    annotation_data = db.N1SeminarRoom825_Annotation
    sensor_data = db.N1SeminarRoom825_data

    ''' Query Activity list '''
    activities = [(d['start_timestamp'], d['end_timestamp'], d['label'], d['avg_n_human']) for d in \
        annotation_data.find({}).sort('date').sort('start_timestamp')]
    # print(activities)

    for activity in activities:
        start_ts, end_ts, label, avg_n_human = activity[0], activity[1], activity[2], activity[3]
        
        ''' Query context and action data'''
        contexts = [(d['timestamp'], d['publisher'], d['name'], d['value']) for d in \
            sensor_data.find({'timestamp': {'$gt': start_ts, '$lt': end_ts}, 'type': 'context'}).sort('timestamp')]
        actions = [(d['timestamp'], d['publisher'], d['name'], None) for d in \
            sensor_data.find({'timestamp': {'$gt': start_ts, '$lt': end_ts}, 'type': 'action'}).sort('timestamp')]

        ''' Data Processing '''
        sensor_values = sorted(contexts + actions, key=lambda x: x[0])
        # sensor_values = list(map(lambda x: list(x) + [label, avg_n_human], sensor_values))
        sensor_table = pd.DataFrame(np.array(sensor_values), columns=['timestamp', 'publisher', 'name', 'value'])
        metadata_header = 'label, start_ts, end_ts, avg_n_human'
        metadata_content = f'{label}, {start_ts}, {end_ts}, {avg_n_human}'
    
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
            f.write(metadata_header+'\n'+metadata_content)
            f.close()

    client.close()

    

if __name__ == '__main__':
    json_file = 'db_info.json'
    with open(json_file, 'r') as f:
        db_info = json.load(f)
    
    query_sensor_activity(db_info)