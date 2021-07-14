import pandas as pd
import numpy as np
import glob

def merge_data(file1, file2, result_path):
    data1 = pd.read_csv(file1, index_col=0)
    data2 = pd.read_csv(file2, index_col=0)
    new_data = data1.append(data2, ignore_index = True)

    new_data.to_csv(result_path, sep=',')

if __name__ == '__main__':
    file1_list = glob.glob('query/before_sum/*-1.csv')
    file2_list = glob.glob('query/before_sum/*-2.csv')
    for i in range(len(file1_list)):
        file1 = file1_list[i]
        file2 = file2_list[i]
        result_file = file1.split('\\')[-1].replace('-1', '')
        result_path = f'query/{result_file}'

        print(file1, file2, result_path)
        merge_data(file1, file2, result_path)

    # file1 = 'query/before_sum/StartAircon0-1.csv'
    # file2 = 'query/before_sum/StartAircon0-2.csv'
    # result_path = 'query/StartAircon0.csv'
    # 