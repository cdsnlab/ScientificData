import os
import sys
import time
import json
import glob
import datetime
import pymongo as pm
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pickle


def single_environment_analysis_from_local(context_name, sensor_dir, zero_remove):
    fnames = glob.glob(f'{sensor_dir}/*')
    task_datas = {'Eating': [], 'Reading': [], 'Phone call': [], 'Seminar': [], 
                    'Lab meeting': [], 'Technical discussion': [], 'Small talk': [], 
                    'Study together': [], 'Eating together': []}

    for fname in fnames:
        label = fname.split('\\')[-1].split('/')[-1].split('_')[0]

        if task_datas.get(label) == None:
            continue

        df = pd.read_csv(fname)
        task_datas[label] = task_datas[label] + list(map(lambda x: float(x), df[df.sensor_name==context_name]['value']))

    if zero_remove:
        for task in task_datas:
            task[task] = list(filter(lambda x: x > 0.0, task[task]))

    sensor_datas = {}
    for task in task_datas:
        sensor_datas[task] = [np.array(task_datas[task])]
        if len(task_datas[task]) == 0: 
            sensor_datas[task].extend(['-', '-', '-'])
        else:
            sensor_datas[task].append(np.mean(sensor_datas[task][0]))
            sensor_datas[task].append(np.median(sensor_datas[task][0]))
            sensor_datas[task].append(np.std(sensor_datas[task][0]))

    return sensor_datas

def single_actuator_analysis_from_local(actuator_name, sensor_dir):
    fnames = glob.glob(f'{sensor_dir}/*')
    task_datas = {'Eating': [], 'Reading': [], 'Phone call': [], 'Seminar': [], 
                    'Lab meeting': [], 'Technical discussion': [], 'Small talk': [], 
                    'Study together': [], 'Eating together': []}

    for fname in fnames:
        label = fname.split('\\')[-1].split('/')[-1].split('_')[0]

        if task_datas.get(label) == None:
            continue

        df = pd.read_csv(fname)
        task_datas[label].append(len(df[df.sensor_name==actuator_name]))

    sensor_datas = {}
    for task in task_datas:
        sensor_datas[task] = [np.array(task_datas[task])]
        if len(task_datas[task]) == 0: 
            sensor_datas[task].extend(['-', '-', '-'])
        else:
            sensor_datas[task].append(np.mean(sensor_datas[task][0]))
            sensor_datas[task].append(np.median(sensor_datas[task][0]))
            sensor_datas[task].append(np.std(sensor_datas[task][0]))

    return sensor_datas

def multi_environment_analysis_from_local(context_names, actuator_names, sensor_dir, zero_remove):
    all_sensor_datas = {}
    for i, context_name in enumerate(context_names):
        print(context_name)
        all_sensor_datas[context_name] = single_environment_analysis_from_local(context_name, sensor_dir, zero_remove)

    for i, actuator_name in enumerate(actuator_names):
        print(actuator_name)
        all_sensor_datas[actuator_name] = single_actuator_analysis_from_local(actuator_name, sensor_dir)

    if zero_remove:
        result_path = 'Distribution/{}_n0.png'
    else:
        result_path = 'Distribution/{}.png'

    tasks = ['Eating', 'Reading', 'Phone call', 'Seminar', 'Lab meeting', 'Technical discussion', 'Small talk', 'Study together', 'Eating together']
    sensor_values = list(map(lambda x: [all_sensor_datas[x][task][0] for task in tasks], context_names+actuator_names))
    summarys = list(map(lambda x: [all_sensor_datas[context][x][1:] for context in context_names+actuator_names], tasks))

    dfs = list(map(lambda x: pd.DataFrame(x, index=context_names+actuator_names, columns=['mean', 'median', 'std']), summarys))
    # writer = pd.ExcelWriter('Distribution/summary.xlsx', engine='xlsxwriter')
    # for i, df in enumerate(dfs):
    #     df.to_excel(writer,
    #                 sheet_name=f'{tasks[i]}',
    #                 na_rep = 'NaN', 
    #                 float_format = "%.3f", 
    #                 header = True, 
    #                 index = True, 
    #                 index_label = "context", 
    #         )
    # writer.save()


    # # green_diamond = dict(markerfacecolor='g', marker='D')
    # for i, context_name in enumerate(context_names+actuator_names):
    #     plt.boxplot(sensor_values[i], 0, '')
    #     # plt.boxplot(sensor_values[i], flierprops=green_diamond)
    #     plt.title(f"Distribution: {context_name}")
    #     plt.xticks(list(range(1, len(tasks)+1)), tasks, fontsize = 5)
    #     plt.gcf().autofmt_xdate()
    #     plt.savefig(result_path.format(context_name), dpi=600)
    #     plt.clf()    
    with open('distribution_pickle.txt', 'wb') as f:
        pickle.dump(sensor_values, f)
        f.close()

    fig = plt.figure()
    senssor_len = len(context_names)
    all_names = context_names+actuator_names
    axs = list(map(lambda x: fig.add_subplot(senssor_len, 1, x+1), range(senssor_len)))
    for i, ax in enumerate(axs):
        ax.boxplot(sensor_values[all_names.index(context_names[i])], 0, '')
        ax.set_ylabel(context_names[i], fontsize = 10, rotation=0, labelpad=15, horizontalalignment='right')
        
    plt.xticks(list(range(1, len(tasks)+1)), tasks, fontsize = 10)
    plt.gcf().autofmt_xdate()
    plt.show()

def single_environment_analysis_from_annotation_task(db_info, context_name, zero_remove, matched=False):
    ''' Data Crawling from Lapras DB '''
    client = pm.MongoClient(db_info['address'])
    client.data.authenticate(db_info['autheticate']['name'], db_info['autheticate']['pw'], mechanism=db_info['autheticate']['mechanism'])
    db = client.data
    annotation_data = db.N1SeminarRoom825_Annotation
    data = db.N1SeminarRoom825_data

    options = {}
    selects = ['start_timestamp', 'end_timestamp', 'label']

    if matched:
        options['matched'] = True
    activities = [tuple(map(lambda x: d[x], selects)) for d in \
        annotation_data.find(options).sort('date').sort('start_timestamp')]

    task_datas = {'Eating': [], 'Reading': [], 'Phone call': [], 'Seminar': [], 
                    'Lab meeting': [], 'Technical discussion': [], 'Small talk': [], 
                    'Study together': [], 'Eating together': []}

    for activity in activities:
        start_ts, end_ts, label = activity[0], activity[1], activity[2]
        if task_datas.get(label) == None:
            continue
        task_datas[label] = task_datas[label] + [d['value'] for d in \
            data.find({'timestamp': {'$gt': start_ts, '$lt': end_ts}, 'name': context_name})]

    client.close()

    if zero_remove:
        for task in task_datas:
            task[task] = list(filter(lambda x: x > 0.0, task[task]))

    sensor_datas = {}
    for task in task_datas:
        sensor_datas[task] = [np.array(task_datas[task])]
        if len(task_datas[task]) == 0: 
            sensor_datas[task].extend(['-', '-', '-'])
        else:
            sensor_datas[task].append(np.mean(sensor_datas[task][0]))
            sensor_datas[task].append(np.median(sensor_datas[task][0]))
            sensor_datas[task].append(np.std(sensor_datas[task][0]))

    return sensor_datas

def multi_environment_analysis_from_annotation_task(db_info, context_names, zero_remove, matched=False):
    all_sensor_datas = {}
    for i, context_name in enumerate(context_names):
        print(context_name)
        all_sensor_datas[context_name] = single_environment_analysis_from_annotation_task(db_info, context_name, zero_remove, matched)

    if zero_remove:
        result_path = 'Distribution/{}_n0.png'
    else:
        result_path = 'Distribution/{}.png'

    tasks = ['Eating', 'Reading', 'Phone call', 'Seminar', 'Lab meeting', 'Technical discussion', 'Small talk', 'Study together', 'Eating together']
    sensor_values = list(map(lambda x: [all_sensor_datas[x][task][0] for task in tasks], context_names))
    summarys = list(map(lambda x: [all_sensor_datas[context][x][1:] for context in context_names], tasks))

    dfs = list(map(lambda x: pd.DataFrame(x, index=context_names, columns=['mean', 'median', 'std']), summarys))
    writer = pd.ExcelWriter('Distribution/summary.xlsx', engine='xlsxwriter')
    for i, df in enumerate(dfs):
        df.to_excel(writer,
                    sheet_name=f'{tasks[i]}',
                    na_rep = 'NaN', 
                    float_format = "%.3f", 
                    header = True, 
                    index = True, 
                    index_label = "context", 
            )
    writer.save()


    green_diamond = dict(markerfacecolor='g', marker='D')
    for i, context_name in enumerate(context_names):
        plt.boxplot(sensor_values[i], flierprops=green_diamond)
        plt.title(f"Distribution: {context_name}")
        plt.xticks(list(range(1, len(tasks)+1)), tasks, fontsize = 5)
        plt.gcf().autofmt_xdate()
        plt.savefig(result_path.format(context_name), dpi=600)
        plt.clf()

def single_environment_analysis_from_annotation(db_info, context_name, zero_remove, matched=False):
    ''' Data Crawling from Lapras DB '''
    client = pm.MongoClient(db_info['address'])
    client.data.authenticate(db_info['autheticate']['name'], db_info['autheticate']['pw'], mechanism=db_info['autheticate']['mechanism'])
    db = client.data
    annotation_data = db.N1SeminarRoom825_Annotation
    data = db.N1SeminarRoom825_data

    options = {}
    selects = ['start_timestamp', 'end_timestamp', 'label']

    if matched:
        options['matched'] = True
    activities = [tuple(map(lambda x: d[x], selects)) for d in \
        annotation_data.find(options).sort('date').sort('start_timestamp')]

    sensor_values = []
    for activity in activities:
        start_ts, end_ts, label = activity[0], activity[1], activity[2]

        sensor_values = sensor_values + [d['value'] for d in \
            data.find({'timestamp': {'$gt': start_ts, '$lt': end_ts}, 'name': context_name})]

    client.close()

    ## Filtering : remove 0 data
    if zero_remove:
        sensor_values = list(filter(lambda x: x > 0.0, sensor_values))
        result_path = f'Distribution/{context_name}_n0.png'
    else:
        result_path = f'Distribution/{context_name}.png'

    sensor_array = np.array(sensor_values)
    sensor_mean = np.mean(sensor_array)
    sensor_median = np.median(sensor_array)
    sensor_std = np.std(sensor_array)

    return sensor_mean, sensor_median, sensor_std


def single_environment_analysis(start_ts, end_ts, db_info, context_name, zero_remove):
    ''' Data Crawling from Lapras DB '''
    client = pm.MongoClient(db_info['address'])
    client.data.authenticate(db_info['autheticate']['name'], db_info['autheticate']['pw'], mechanism=db_info['autheticate']['mechanism'])
    db = client.data
    data = db.N1SeminarRoom825_data

    sensor_values = [d['value'] for d in \
        data.find({'timestamp': {'$gt': start_ts, '$lt': end_ts}, 'name': context_name})]

    client.close()

    ## Filtering : remove 0 data
    if zero_remove:
        sensor_values = list(filter(lambda x: x > 0.0, sensor_values))
        result_path = f'Distribution/{context_name}_n0.png'
    else:
        result_path = f'Distribution/{context_name}.png'

    sensor_array = np.array(sensor_values)
    sensor_mean = np.mean(sensor_array)
    sensor_median = np.median(sensor_array)
    sensor_std = np.std(sensor_array)

    return sensor_mean, sensor_median, sensor_std


if __name__ == '__main__':
    start_ts = int(time.mktime(datetime.datetime(2017, 9, 1, 0, 0).timetuple())*1000)
    end_ts = int(time.mktime(datetime.datetime(2018, 1, 1, 0, 0).timetuple())*1000)

    json_file = 'info/db_info.json'
    with open(json_file, 'r') as f:
        db_info = json.load(f)
        f.close()

    with open('info/env_con_list.txt', 'r') as f:
        text = f.read().strip()
        contexts = text.split('\n')
        f.close()

    with open('info/act_con_list.txt', 'r') as f:
        text = f.read().strip()
        actuators = text.split('\n')
        f.close()

    zero_remove = False
    matched = False
    # results = np.zeros((len(contexts), 3), dtype=np.float64)
    

    # for i, context_name in enumerate(contexts):
    #     sensor_mean, sensor_median, sensor_std = single_environment_analysis(start_ts, end_ts, db_info, context_name, zero_remove)
    #     results[i, 0] = sensor_mean
    #     results[i, 1] = sensor_median
    #     results[i, 2] = sensor_std

    # for i, context_name in enumerate(contexts):
    #     sensor_mean, sensor_median, sensor_std = single_environment_analysis_from_annotation(db_info, context_name, zero_remove, matched)
    #     results[i, 0] = sensor_mean
    #     results[i, 1] = sensor_median
    #     results[i, 2] = sensor_std

    # result_fname = f'Distribution/summary.xlsx'
    # result_df = pd.DataFrame(results, index=contexts, columns=['mean', 'median', 'std'])
    # result_df.to_excel(result_fname,
    #                 sheet_name='Sheet1',
    #                 na_rep = 'NaN', 
    #                 float_format = "%.3f", 
    #                 header = True, 
    #                 index = True, 
    #                 index_label = "context", 
    #         )

    # for i, context_name in enumerate(contexts):
    #     print(context_name)
    #     single_environment_analysis_from_annotation_task(db_info, context_name, zero_remove, matched)

    # multi_environment_analysis_from_annotation_task(db_info, contexts, zero_remove, matched)
    sensor_dir = 'sensor'
    multi_environment_analysis_from_local(contexts, actuators, sensor_dir, zero_remove)


