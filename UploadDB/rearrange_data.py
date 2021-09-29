import os
import glob
import shutil

def meta_processing():
    meta_path = 'metadata'
    meta_list = glob.glob(meta_path+'/*')

    for meta in meta_list:
        new_text = ''
        with open(meta, 'r') as f:
            texts = f.readlines()
            for i in range(len(texts)):
                texts[i] = texts[i].replace('\n', ' ')
            texts = list(filter(lambda x: x != ' ', texts))
            new_text = '\n'.join(texts)
            f.close()
        
        with open(meta, 'w') as f:
            f.write(new_text)
            f.close()

def rearrange_data():
    sensor_path = 'sensor'
    meta_path = 'metadata'
    new_path = 'ScientificData'
    labels = ['Eating', 'Reading', 'Phone call', 'Small talk', 'Eating together', 
            'Seminar', 'Study together', 'Lab meeting', 'Technical discussion']
    if not os.path.isdir(new_path):
        os.makedirs(new_path)

    sensor_dicts = {}
    meta_dicts = {}
    meta_list = glob.glob(meta_path+'/*')
    sensor_list = glob.glob(sensor_path+'/*')

    # print(meta_list)
    # print(sensor_list)
    for label in labels:
        meta_dicts[label] = []
        sensor_dicts[label] =[]

    for meta in meta_list:
        meta_dicts[meta.split('\\')[-1].split('_')[0]].append(meta)

    for sensor in sensor_list:
        sensor_dicts[sensor.split('\\')[-1].split('_')[0]].append(sensor)
    
    for label in labels:
        meta_dicts[label] = sorted(meta_dicts[label])
        sensor_dicts[label] = sorted(sensor_dicts[label])

    for label in labels:
        activity_path = f'{new_path}/{label}'
        if not os.path.isdir(activity_path):
            os.makedirs(activity_path)
            os.makedirs(f'{activity_path}/metadata')
            os.makedirs(f'{activity_path}/sensor')

        for i in range(len(meta_dicts[label])):
            meta_path = meta_dicts[label][i]
            sensor_path = sensor_dicts[label][i]
            new_meta_path = f'{activity_path}/metadata/' + meta_path.split('\\')[-1].split('_')[0] + f'_{i}.txt'
            new_sensor_path = f'{activity_path}/sensor/' + sensor_path.split('\\')[-1].split('_')[0] + f'_{i}.csv'
            shutil.copy(meta_path, new_meta_path)
            shutil.copy(sensor_path, new_sensor_path)



if __name__ == '__main__':
    meta_processing()
    rearrange_data()