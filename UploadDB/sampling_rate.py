import os
import sys
import glob
import pandas as pd
import numpy as np
import random
import matplotlib.pyplot as plt

def sr_calculate(df):
    timestamps = np.array(df['timestamp'])
    if timestamps.shape[0] < 2:
        avg_sr = np.nan
    else:
        start_ts = timestamps[:-1]
        end_ts = timestamps[1:]
        avg_sr = np.mean((end_ts-start_ts)/1000)
    return avg_sr

def detect_wrong(df):
    candidate_columns = ['Brightness_1', 'Humidity_1', 'Temperature_1', 'Brightness_2', 'Humidity_2', 'Temperature_2']
    result = list(filter(lambda x: df[x] > 20, candidate_columns)) 
    return result

def convert_relativepath(fname, root_dir):
    activity = fname.split('_')[0]
    return f'{root_dir}/{activity}/sensor/{fname}'

def sr_analysis(context_names, root_dir):
    activities = os.listdir(root_dir)
    result = {}
    for activity in activities:
        print(activity)
        sensor_dir = f'{root_dir}/{activity}/sensor'
        fnames = sorted(os.listdir(sensor_dir), key=lambda x: int(x.split('_')[-1].split('.')[0]))
        activity_srs = []
        
        for fname in fnames:
            df = pd.read_csv(f'{sensor_dir}/{fname}')
            srs = list(map(lambda x: sr_calculate(df[df.sensor_name==x]), context_names))
            activity_srs.append(srs)
            
        sr_df = pd.DataFrame(np.array(activity_srs), columns=context_names)
        result[activity] = sr_df

    writer = pd.ExcelWriter('DoRe_sr.xlsx', engine='xlsxwriter')
    for activity in activities:
        result[activity].to_excel(writer, sheet_name=activity, index=None)
    writer.save()

def sr_analysis_merge(context_names, root_dir):
    activities = os.listdir(root_dir)
    result = []
    for activity in activities:
        print(activity)
        sensor_dir = f'{root_dir}/{activity}/sensor'
        fnames = sorted(os.listdir(sensor_dir), key=lambda x: int(x.split('_')[-1].split('.')[0]))
        activity_srs = []
        
        for fname in fnames:
            df = pd.read_csv(f'{sensor_dir}/{fname}')
            srs = [fname] + list(map(lambda x: sr_calculate(df[df.sensor_name==x]), context_names))
            activity_srs.append(srs)
            
        sr_df = pd.DataFrame(np.array(activity_srs), columns=['filename'] + context_names)
        result.append(sr_df)

    result_df = pd.concat(result)
    writer = pd.ExcelWriter('DoRe_sr_merge.xlsx', engine='xlsxwriter')
    result_df.to_excel(writer, sheet_name='sheet1', index=None)
    writer.save()


def sr_filtering(fname):
    df = pd.read_excel(fname)
    mask = (df.Brightness_1 > 20) | (df.Brightness_2 > 20) | (df.Temperature_1 > 20) | (df.Temperature_2 > 20) | (df.Humidity_1 > 20) | (df.Humidity_2 > 20)

    df_filtered = df.loc[mask, :]
    print(df_filtered)

    writer = pd.ExcelWriter('DoRe_sr_filtering.xlsx', engine='xlsxwriter')
    df_filtered.to_excel(writer, sheet_name='filtered', index=None)
    writer.save()

def timestamp_generator(prev_ts, next_ts):
    interval = int((next_ts-prev_ts)/20)
    timestamps = list(map(lambda x, y: x + interval*y + random.randint(-5, 5), [int(prev_ts)]*19, range(1, 20)))
    return timestamps

def first_timestamp_generator(start_ts, first_ts, interval):
    timestamps = list(map(lambda x, y: x - interval*y + random.randint(-5, 5), [int(first_ts)]*19, range(1, 20)))
    timestamps = list(filter(lambda x: x >= start_ts, timestamps))
    return timestamps

def last_timestamp_generator(end_ts, last_ts, interval):
    timestamps = list(map(lambda x, y: x + interval*y + random.randint(-5, 5), [int(last_ts)]*19, range(1, 20)))
    timestamps = list(filter(lambda x: x <= end_ts, timestamps))
    return timestamps


def value_generator(prev_value, next_value, count):
    avg_value = (float(prev_value)+float(next_value))/2
    values = [avg_value]*count
    return values

def sr_fixation(fname, root_dir):
    df = pd.read_excel(fname)
    print(df)
    df_len = len(df)
    print(len(df))
    df_columns = ['timestamp', 'sensor_name', 'value']
    for i in range(df_len):
        line = df.loc[i]
        wrongs = detect_wrong(line)
        wrong_df = pd.read_csv(convert_relativepath(line['filename'], root_dir))
        start_ts = wrong_df.iloc[0]['timestamp']
        end_ts = wrong_df.iloc[-1]['timestamp']
        print(start_ts, end_ts)
        print(wrong_df)
        print(len(wrong_df))
        
        for wrong in wrongs:
            wrong_context = wrong_df[wrong_df.sensor_name==wrong]
            wrong_names = [wrong]*19

            for j in range(len(wrong_context)-1):
                prev_line = wrong_context.iloc[j]
                next_line = wrong_context.iloc[j+1]
                new_timestamps = timestamp_generator(prev_line['timestamp'], next_line['timestamp'])
                new_values = value_generator(prev_line['value'], next_line['value'], 19)
                new_data = list(map(lambda x, y, z: [x, y, z], new_timestamps, wrong_names, new_values))
                new_df = pd.DataFrame(new_data, columns=df_columns)
                wrong_df = wrong_df.append(new_df)


            wrong_df = wrong_df.sort_values(by=['timestamp'])
            avg_interval = np.mean(np.array(wrong_df[wrong_df.sensor_name==wrong]['timestamp'].iloc[1:]) - np.array(wrong_df[wrong_df.sensor_name==wrong]['timestamp'].iloc[:-1]))
            
            wrong_df = wrong_df.append(new_df)
            wrong_df = wrong_df.sort_values(by=['timestamp'])
            
            ''' End point fixation '''
            new_timestamps = last_timestamp_generator(end_ts, wrong_context.iloc[-1]['timestamp'], avg_interval)
            new_values = value_generator(wrong_context.iloc[-1]['value'], wrong_context.iloc[-1]['value'], len(new_timestamps))
            new_data = list(map(lambda x, y, z: [x, y, z], new_timestamps, wrong_names, new_values))
            new_df = pd.DataFrame(new_data, columns=df_columns)
            wrong_df = wrong_df.append(new_df)
            wrong_df = wrong_df.sort_values(by=['timestamp'])

        wrong_df.to_csv(convert_relativepath(line['filename'], root_dir), index=None)

def sr_statistics(context_names, root_dir):
    activities = os.listdir(root_dir)
    result = []
    for activity in activities:
        print(activity)
        sensor_dir = f'{root_dir}/{activity}/sensor'
        fnames = sorted(os.listdir(sensor_dir), key=lambda x: int(x.split('_')[-1].split('.')[0]))
        activity_srs = []
        
        for fname in fnames:
            df = pd.read_csv(f'{sensor_dir}/{fname}')
            srs = list(map(lambda x: sr_calculate(df[df.sensor_name==x]), context_names))
            activity_srs.append(srs)
            
        sr_df = pd.DataFrame(np.array(activity_srs), columns=context_names)
        result.append(sr_df)

    result_df = pd.concat(result)
    print(result_df[context_names[4]])
    plt.hist(result_df[result_df[context_names[4]] > 5][context_names[4]].dropna())
    plt.show()
    # writer = pd.ExcelWriter('DoRe_sr_merge.xlsx', engine='xlsxwriter')
    # result_df.to_excel(writer, sheet_name='sheet1', index=None)
    # writer.save()

if __name__ == '__main__':
    with open('info/env_con_list.txt') as f:
        context_names = f.read().strip().split('\n')
        f.close()
    root_dir = 'ScientificData'
    xlsx_fname = 'DoRe_sr_merge.xlsx'
    fliter_name = 'DoRe_sr_filtering.xlsx'
    # sr_analysis(context_names, root_dir)
    # sr_analysis_merge(context_names, root_dir)
    # sr_filtering(xlsx_fname)
    # sr_fixation(fliter_name, root_dir)
    sr_statistics(context_names, root_dir)

    