import os
import sys
import glob
import pandas as pd

def add_sensor_name(spath, mpath):
    fnames = os.listdir(mpath)
    for fname in fnames:
        meta_fname = f'{mpath}/{fname}'
        sensor_fname = f'{spath}/{fname}'.replace('.txt', '.csv')
        df = pd.read_csv(sensor_fname)
        try:
            sensor_names = list(set(df['sensor_name']))
            if len(sensor_names) < 3:
                print(f'remove: {sensor_fname}, {meta_fname}')
                os.remove(sensor_fname)
                os.remove(meta_fname)
                continue
            sensor_names = sorted(sensor_names)
        except:
            print(fname)
            print(list(set(df['sensor_name'])))
            sys.exit()
        next_context = ', '.join(sensor_names)
        with open(meta_fname, 'r') as f:
            prev_content_list = f.readlines()
            f.close()
        prev_content = ''.join(prev_content_list[:5])

        try: 
            with open(meta_fname, 'w') as f:
                    f.write(prev_content+'sensors: '+next_context)
                    f.close()
        except:
            print(prev_content)
            print(next_context)
            sys.exit()



if __name__ == '__main__':
    spath, mpath = 'sensor', 'metadata'
    add_sensor_name(spath, mpath)