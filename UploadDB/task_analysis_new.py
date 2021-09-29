import os
import sys
import pandas as pd
import numpy as np

def return_result(sensor_data, environment_list, actuator_list):
    fname = sensor_data[0]
    env_data = sensor_data[1]
    act_data = sensor_data[2]
    result_list = [fname]
    result_list = result_list + list(map(lambda x: env_data.count(x), environment_list))
    result_list = result_list + list(map(lambda x: act_data.count(x), actuator_list))
    return result_list


def task_analysis(data_path, actuator_list, environment_list, single_tasks, projector_tasks, ignore_brightness=False):
    fnames = os.listdir(data_path)

    task_to_fname = {}
    for fname in fnames:
        task_name = fname.split('_')[0]
        if task_to_fname.get(task_name) == None:
            task_to_fname[task_name] = []
        task_to_fname[task_name].append(fname)

    tasks = task_to_fname.keys()
    task_to_sensor = {}


    print(tasks)
    print(single_tasks, projector_tasks)

    for task_name, related_fnames in task_to_fname.items():
        print(task_name)
        print(len(related_fnames))

        task_to_sensor[task_name] = []
        for fname in related_fnames:
            sensor_df = pd.read_csv(f'{data_path}/{fname}')
            sensors = list(set(sensor_df['sensor_name']))
            environment_agents = list(filter(lambda x: x in environment_list, sensors))
            actuator_agents = list(filter(lambda x: x in actuator_list, sensors))

            task_to_sensor[task_name].append([fname, environment_agents, actuator_agents])

            brightness_medians = [sensor_df[sensor_df.name =='Brightness_1']['value'].median(), \
                sensor_df[sensor_df.name =='Brightness_2']['value'].median()]

            if brightness_medians[0] == np.NaN or brightness_medians[0] < 3:
                task_to_sensor[task_name][-1][1].remove('Brightness_1')

            if brightness_medians[1] == np.NaN or brightness_medians[1] < 3:
                task_to_sensor[task_name][-1][1].remove('Brightness_2')
        
        if task_name in projector_tasks:
            if ignore_brightness:
                task_to_sensor[task_name] = sorted(task_to_sensor[task_name], key=lambda x: (x[2].count('Projector'), len(x[1]), (x[1].count('Sound_L')+x[1].count('Sound_C')+x[1].count('Sound_R')), len(x[2])), reverse=True)
            else: 
                task_to_sensor[task_name] = sorted(task_to_sensor[task_name], key=lambda x: (-(x[3].count(0.0)+x[3].count(np.NaN)), x[2].count('Projector'), len(x[1]), (x[1].count('Sound_L')+x[1].count('Sound_C')+x[1].count('Sound_R')), len(x[2])), reverse=True)
        else:
            if ignore_brightness:
                task_to_sensor[task_name] = sorted(task_to_sensor[task_name], key=lambda x: (len(x[1]), (x[1].count('Sound_L')+x[1].count('Sound_C')+x[1].count('Sound_R')), len(x[2])), reverse=True)
            else:
                task_to_sensor[task_name] = sorted(task_to_sensor[task_name], key=lambda x: (-(x[3].count(0.0)+x[3].count(np.NaN)), len(x[1]), (x[1].count('Sound_L')+x[1].count('Sound_C')+x[1].count('Sound_R')), len(x[2])), reverse=True)

    if not os.path.isdir('analysis'):
        os.makedirs('analysis')

    with open('analysis/analysis_result.txt', 'w') as f:
        for task_name, sensor_datas in task_to_sensor.items():
            f.write(f'{task_name}+\n\n')
            for sensor in sensor_datas:
                f.write(str(sensor)+'\n')
            f.write('\n\n')
        f.close()

    filtered_all_sensors = []
    for task_name, sensor_datas in task_to_sensor.items(): 
        if task_name in projector_tasks:
            if ignore_brightness:
                filtered_sensors = list(map(lambda x: return_result(x, environment_list, actuator_list), filter(lambda x: len(x[1]) > 1, sensor_datas)))
            else: 
                filtered_sensors = list(map(lambda x: return_result(x, environment_list, actuator_list), filter(lambda x: (x[3].count(0.0)+x[3].count(np.NaN)) == 0, sensor_datas)))
        else:
            if ignore_brightness:
                filtered_sensors = list(map(lambda x: return_result(x, environment_list, actuator_list), filter(lambda x: len(x[1]) > 1, sensor_datas)))
            else:
                filtered_sensors = list(map(lambda x: return_result(x, environment_list, actuator_list), filter(lambda x: (x[3].count(0.0)+x[3].count(np.NaN)) == 0, sensor_datas)))
        filtered_all_sensors = filtered_all_sensors + filtered_sensors


    result_fname = 'analysis/sorted_episodes.csv'
    all_sensors_array = np.array(filtered_all_sensors)
    all_sensor_df = pd.DataFrame(all_sensors_array, columns=['fname']+environment_list+actuator_list)
    all_sensor_df.to_csv(result_fname,
                    na_rep = 'NaN', 
                    header = True, 
                    index=False
            )


        

if __name__ == '__main__': 
    data_path = 'sensor'

    with open('info/environment_list.txt') as f:
        text = f.read().strip()
        environment_list = text.split('\n')
        f.close()

    with open('info/actuator_list.txt') as f:
        text = f.read().strip()
        actuator_list = text.split('\n')
        f.close()
    
    with open('info/single_tasks.txt') as f:
        text = f.read().strip()
        single_tasks = text.split('\n')
        f.close()

    with open('info/projector_tasks.txt') as f:
        text = f.read().strip()
        projector_tasks = text.split('\n')
        f.close()
    print(actuator_list, environment_list)
    
    ignore_brightness = True

    task_analysis(data_path, actuator_list, environment_list, single_tasks, projector_tasks, ignore_brightness)

