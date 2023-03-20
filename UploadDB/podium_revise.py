import os
import sys
import shutil
import pandas as pd

CURR_DIR = os.path.abspath(os.path.dirname(__file__))
ORI_DATASET_DIR = os.path.join(CURR_DIR, 'ScientificData')
REVISED_DATASET_DIR = os.path.join(CURR_DIR, 'DOO-RE')
# print(ORI_DATASET_DIR)

if __name__ == '__main__':
    print(ORI_DATASET_DIR)
    print(REVISED_DATASET_DIR)

    shutil.copytree(ORI_DATASET_DIR, REVISED_DATASET_DIR)

    tasks = os.listdir(REVISED_DATASET_DIR)
    for task in tasks:
        print(task)
        sensor_dir = os.path.join(os.path.join(REVISED_DATASET_DIR, task), 'sensor')
        # print(sensor_dir)
        sensor_fnames = os.listdir(sensor_dir)
        # print(sensor_fnames)
        for sensor_fname in sensor_fnames:
            sensor_fpath = os.path.join(sensor_dir, sensor_fname)
            df = pd.read_csv(sensor_fpath)
            df.loc[(df.sensor_name == 'PodiumIR'), 'value'] = \
                df.loc[(df.sensor_name == 'PodiumIR'), 'value'].apply(
                lambda x: 2.076/(int(x)/1000 - 0.011)
            )
            # print(df.loc[(df.sensor_name == 'PodiumIR'), :])
            # sys.exit()
            df.to_csv(sensor_fpath, index=None)

