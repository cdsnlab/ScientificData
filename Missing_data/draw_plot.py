import datetime
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import sys


def draw_heatmap(file_path, fname, start_dt, end_dt, method='alive', index_name='sensor'):
    df = pd.read_excel(file_path, sheet_name='Sheet1', index_col=index_name)
    start = start_dt.strftime('%y/%m/%d')
    end = end_dt.strftime('%y/%m/%d')
    columns = list(df.columns)
    start_index = columns.index(start)
    end_index = columns.index(end)
    df = df.iloc[:, list(range(start_index, end_index+1))]

    if method == 'max':
        for i in range(len(df)):
            row = df.iloc[i]
            if row.max() > 0:
                df.iloc[i] = row/row.max()
                # df.iloc[i] = row

    elif method == 'mean':
        for i in range(len(df)):
            row = df.iloc[i]
            if row.mean() > 0:
                df.iloc[i] = (row/row.mean()).clip(0, 1)

    elif method == 'alive':
        for i in range(len(df)):
            df.iloc[i] = df.iloc[i].clip(0, 1)
    else:
        print(f'wrong method - {method}')
        sys.exit()
        

    sns.set(font_scale=0.4)
    color_bar_title = 'Sensor readings received as proportion of expected'
    ax = sns.heatmap(df, xticklabels=1, cbar_kws={'label': color_bar_title})

    xlabels = ax.get_xticklabels()
    xmonths = list(filter(lambda x: x.get_text()[-2:] == '01', xlabels))
    xpositions = list(map(lambda x: x.get_position()[0], xmonths))
    xtexts = list(map(lambda x: x.get_text()[:-3], xmonths))
    plt.xticks(xpositions, xtexts)

    plt.title('Seminar Room - Missing data', fontsize=10)
    plt.savefig(fname, dpi = 600)
    plt.clf()


if __name__ == '__main__':
    # file_path = '170101-210701_context.xlsx'
    # index_name = 'context'
    # file_path = '170101-210701_sensor.xlsx'  
    # file_path = '170101-210701_sensor_merge.xlsx'  
    # file_path = '170101-210701_sensor_custom.xlsx'  
    # file_path = '170901-180101_overall.xlsx'
    file_path = '210401-211001_context.xlsx'
    # index_name = 'sensor'
    index_name = 'context'
    # index_name = 'task'
    # index_name = 'overall'

    start_dt = datetime.datetime(2021, 4, 1, 0, 0)
    end_dt = datetime.datetime(2021, 10, 1, 0, 0)
    
    methods = ['max', 'mean', 'alive']
    for method in methods:
        fname = start_dt.strftime('%y%m%d')+'-'+end_dt.strftime('%y%m%d')+f'_{method}.png'
        draw_heatmap(file_path, fname, start_dt, end_dt, method=method, index_name=index_name)

