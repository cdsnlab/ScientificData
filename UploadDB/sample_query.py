import os
import sys
import shutil
import pandas as pd


def sample_query(list_path, result_path, data_path, meta_path):
    df = pd.read_excel(list_path, header=None, sheet_name=None)

    if not os.path.isdir(result_path):
        os.makedirs(result_path)
    

    for sheet_name, data in df.items():
        sample_list = list(data[0])

        if not os.path.isdir(f'{result_path}/{sheet_name}'):
            os.makedirs(f'{result_path}/{sheet_name}')

        for fname in sample_list:
            meta_name = fname.replace('.csv', '.txt')
            shutil.copyfile(f'{data_path}/{fname}', f'{result_path}/{sheet_name}/{fname}')
            shutil.copyfile(f'{meta_path}/{meta_name}', f'{result_path}/{sheet_name}/{meta_name}')


if __name__ == '__main__':
    list_path = 'sample_list.xlsx'
    result_path = 'samples'
    data_path = 'sensor'
    meta_path = 'metadata'
    sample_query(list_path, result_path, data_path, meta_path)