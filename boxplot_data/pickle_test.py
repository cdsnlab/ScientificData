import pickle
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd



def pickle_plot():
    with open('distribution_pickle2.txt', 'rb') as f:
        sensor_values = pickle.load(f)
        f.close()

    with open('info/env_con_list.txt', 'r') as f:
        text = f.read().strip()
        context_names = text.split('\n')
        f.close()

    with open('info/act_con_list.txt', 'r') as f:
        text = f.read().strip()
        actuator_names = text.split('\n')
        f.close()

    # tasks = ['Eating', 'Reading', 'Phone call', 'Seminar', 'Lab meeting', 'Technical discussion', 'Small talk', 'Study together', 'Eating together']
    tasks = ['Eating', 'Reading', 'Phone call', 'Seminar', 'Lab meeting', 'Technical discussion', 'Small talk', 'Study together', 'Eating together']
    task_order = [
        'Eating', 
        'Phone call', 
        'Reading', 
        'Small talk', 
        'Study together', 
        'Eating together',
        'Lab meeting', 
        'Seminar', 
        'Technical discussion', 
    ]
    all_names = context_names+actuator_names
    sensor_len = len(context_names)
    # name_order = [
    #     'Brightness_1', 
    #     'Humidity_1',
    #     'Temperature_1',
    #     'Sound_L',
    #     'Sound_P',
    #     'PodiumIR'
    # ]

    name_order = [
        'Brightness_1', 
        'Humidity_1',
        'Temperature_1',
        'Sound_L',
        'Sound_P',
        'PodiumIR'
    ]


    ### Draw Boxplot ###
    # fig = plt.figure(figsize=(20, 20))
    # axs = list(map(lambda x: fig.add_subplot(sensor_len, 1, x+1), range(sensor_len)))
    

    print(len(sensor_values), type(sensor_values))

    sensor_types = {
        'Sound_C': 'sound',
        'Sound_R': 'sound',
        'Sound_L': 'sound',
        'Brightness_1': 'brightness',
        'Humidity_1': 'humidity',
        'Temperature_1': 'temperature',
        'Brightness_2': 'brightness',
        'Humidity_2': 'humidity',
        'Temperature_2': 'temperature',
        'PodiumIR': 'podium_ir',
        'Sound_P': 'podium_sound'
    }
    task_types = {
        'Eating': 'individual', 
        'Reading': 'individual', 
        'Phone call': 'individual', 
        'Seminar': 'group', 
        'Lab meeting': 'group', 
        'Technical discussion': 'group', 
        'Small talk': 'group', 
        'Study together': 'group', 
        'Eating together': 'group'
    }

    columns = ['category', 'sensor_type', 'sensor_name', 'task_type', 'task', 'presenter', 'value']
    sensor_type_list = ['sound', 'brightness', 'humidity', 'temperature', 'podium_ir', 'podium_sound']
    task_type_list = ['individual', 'group']
    intervals = context_names
    events = actuator_names
    categories = ['interval', 'event']
    
    sensor_table = []
    for sensor_name in context_names:
        
        sensor_type = sensor_types[sensor_name]
        task_data = sensor_values[all_names.index(sensor_name)]
        category = categories[0] if sensor_name in intervals else categories[1]
        # print(sensor_name, sensor_type, len(task_data))
        for task, values in zip(tasks, task_data):
            # print(task, len(values))
            task_type = task_types[task]
            presenter = False
            if task in ['Seminar', 'Lab meeting']:
                presenter = True
            sensor_table = sensor_table + [(category, sensor_type, sensor_name, task_type, task, presenter, values[i]) for i in range(len(values))]

    sensor_df = pd.DataFrame(data=sensor_table, columns=columns)
    # sensor_df[sensor_df.sensor_name == 'PodiumIR']['value'] = sensor_df[sensor_df.sensor_name == 'PodiumIR']['value'].apply(lambda x: 2.076/(x/1000 - 0.011))
    # sensor_df.loc[(sensor_df.sensor_name == 'PodiumIR'), 'value'] = sensor_df.loc[(sensor_df.sensor_name == 'PodiumIR'), 'value'].apply(lambda x: 2.076/(x/1000 - 0.011))
    

    print(sensor_df)
    print(sensor_df[sensor_df.sensor_name == 'PodiumIR'])
    # print(sensor_df[sensor_df.sensor_name == 'PodiumIR']['value'].apply(lambda x: 2.076/(x/1000 - 0.011)))

    # event_sensor_type_list = list(set([event.split('_')[0] for event in events]))
    # print(event_sensor_type_list)
    # event_cloumns = ['category', 'sensor_type', 'sensor_name', 'task_type', 'task', 'presenter', 'count']
    # event_table = []
    # for sensor_name in events:
    #     sensor_type = sensor_name.split('_')[0]
    #     task_data = sensor_values[all_names.index(sensor_name)]
    #     category = categories[0] if sensor_name in intervals else categories[1]
    #     for task, counts in zip(tasks, task_data):
    #         # print(task, len(values))
    #         task_type = task_types[task]
    #         presenter = False
    #         if task in ['Seminar', 'Lab meeting']:
    #             presenter = True
    #         event_table = event_table + [(category, sensor_type, sensor_name, task_type, task, presenter, counts[i]) for i in range(len(counts))]

    # event_df = pd.DataFrame(data=event_table, columns=event_cloumns)
    # print(event_df)


    # sns.boxplot(data=sensor_df, x='task_type', y='value', hue='sensor_type')
    # plt.show()

    # filtered = sensor_df.sensor_name.isin(['Sound_L', 'Brightness_1', 'Humidity_1', 'Temperature_1', 'PodiumIR', 'Sound_P'])
    filtered_list = name_order
    fig, axes = plt.subplots(nrows=len(filtered_list), ncols=1)
    axes = axes.flatten()
    
    for sensor_name, axe in zip(filtered_list, axes):
        sns.boxplot(
            data=sensor_df[sensor_df.sensor_name == sensor_name], 
            x='task', 
            y='value', 
            # hue='sensor_name',
            ax=axe,
            order=task_order
        )
        axe.set_ylabel(sensor_name, fontsize = 10, rotation=0, labelpad=15, horizontalalignment='right')
        axe.set_xlabel(None)
        if sensor_name == 'PodiumIR':
            axe.set_ylim(0, 50)
    # plt.subplots_adjust(left=0.08, bottom=0.02, right=0.98, top=0.98, wspace=None, hspace=0.00)
    plt.show()
    plt.clf()


    # filtered_list = ['PodiumIR']

    # sns.boxplot(
    #     data=sensor_df[sensor_df.sensor_name == filtered_list[0]], 
    #     x='task', 
    #     y='value', 
    #     # hue='sensor_name',
    #     order=task_order
    # )
    # plt.ylim(0, 50)
    # plt.show()
    # plt.clf()
    # fig.clear()


    # fig, axes = plt.subplots(nrows=len(sensor_type_list), ncols=1)
    # fig, axes = plt.subplots(nrows=1, ncols=len(sensor_type_list))
    # axes = axes.flatten()

    # for sensor_type, axe in zip(sensor_type_list, axes):
    #     sns.boxplot(
    #         data=sensor_df[sensor_df.sensor_type == sensor_type], 
    #         x='task_type', 
    #         y='value', 
    #         hue='sensor_name',
    #         ax=axe
    #     )

    # plt.show()
    # plt.clf()
    # fig.clear()

    # sns.boxplot(
    #     data=sensor_df[sensor_df.sensor_type == 'sound'], 
    #     x='task_type', 
    #     y='value', 
    #     hue='sensor_name',
    # )
    # plt.legend(loc='best', ncol=3)
    # plt.show()
    # plt.clf()


    # sns.boxplot(
    #     data=sensor_df[sensor_df.sensor_name == 'PodiumIR'], 
    #     x='presenter', 
    #     y='value', 
    #     hue='sensor_name',
    # )
    # plt.legend(loc='best', ncol=3)
    # plt.show()
    # plt.clf()





    # for i, ax in enumerate(axs):
    #     sns_ax = sns.boxplot(data=sensor_values[all_names.index(context_names[i])], ax=ax, palette="Set3")
    #     sns_ax.set_xticklabels(tasks)
    #     ax.set_ylabel(context_names[i], fontsize = 10, rotation=0, labelpad=15, horizontalalignment='right')
        
    # plt.subplots_adjust(left=0.08, bottom=0.02, right=0.98, top=0.98, wspace=None, hspace=0.00)
    # plt.show()


    # ## Pickle data to raw excel data ###
    # with pd.ExcelWriter("./boxplot_distribution.xlsx") as writer: 
    #     for context_name in all_names:
    #         data = sensor_values[all_names.index(context_name)]            
    #         df = pd.DataFrame(data, index=tasks).transpose()
    #         df.to_excel(writer, sheet_name=context_name, index=False) 


    # # Pickle data to raw excel data ###
    # with pd.ExcelWriter("./boxplot_summary.xlsx") as writer: 
    #     for context_name in all_names:
    #         data = sensor_values[all_names.index(context_name)]            
    #         df = pd.DataFrame(data, index=tasks).transpose()
    #         mean = df.mean().transpose()
    #         std = df.std().transpose()
    #         median = df.median().transpose()
    #         max = df.max().transpose()
    #         min = df.min().transpose()
    #         q1 = df.quantile(q=0.25).transpose()
    #         q3 = df.quantile(q=0.75).transpose()

    #         analyzed_df = pd.DataFrame([mean, std, median, max, min, q1, q3], index=['mean', 'std', 'median', 'max', 'min', 'q1', 'q3'], columns=tasks)
    #         analyzed_df.to_excel(writer, sheet_name=context_name) 
    


if __name__ == '__main__':
    pickle_plot()