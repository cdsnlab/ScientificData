import os
import glob
import pandas as pd

AMBIENT = ('Brightness_1', 'Humidity_1', 'Temperature_1', 'Brightness_2', 'Humidity_2', 'Temperature_2')
LIGHT = ('Light_1', 'Light_2', 'Light_3')
MONNIT = ('Motion_1', 'Motion_2', 'Motion_3', 'Motion_4', 'Motion_5', 'Motion_6', 'Motion_7', 'Motion_8', 'Seat_1', 'Seat_2', 'Seat_3', 'Seat_4', 'Seat_5', 'Seat_6', 'Seat_7','Seat_8', 'Seat_9', 'Seat_10', 'Seat_11', 'Seat_12')
PODIUM = ('PodiumIR', 'Sound_P')
PROJECTOR = ('Projector')
DOOR = ('Door')
SOUND = ('Sound_C', 'Sound_L', 'Sound_R')
AIRCON = ('Aircon_1', 'Aircon_2')

ENV_SENSORS = (AMBIENT, MONNIT, PODIUM, SOUND)

def data_filter(time_thres):
    meta_path = 'metadata'
    sensor_path = 'sensor'
    metas = glob.glob(f'{meta_path}/*')
    sensors = glob.glob(f'{sensor_path}/*')
    
    remove_list = []
    time_filtered = []
    print(len(metas), len(sensors))

    ''' Filtering by duration '''
    for i, meta in enumerate(metas):
        with open(meta, 'r') as f:
            texts = f.readlines()
            duration = int(texts[4].strip().split(' ')[-1])
            f.close()
        
        if duration < time_thres:
            time_filtered.append((i, meta))

    print(time_filtered)

    for _, x in enumerate(reversed(time_filtered)):
        print(x)
        remove_list.append((metas.pop(x[0]), sensors.pop(x[0])))
        print(remove_list[-1])
        
    print(len(metas), len(sensors))

    print(len(metas), len(sensors))
    print(remove_list)
    for target in remove_list:
        os.remove(target[0])
        os.remove(target[1])

if __name__ == '__main__':
    time_thres = 60*5 # Neet at least 5 minute duration
    data_filter(time_thres)
