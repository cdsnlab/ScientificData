import pickle
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd



def pickle_plot():
    with open('distribution_pickle.txt', 'rb') as f:
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

    tasks = ['Eating', 'Reading', 'Phone call', 'Seminar', 'Lab meeting', 'Technical discussion', 'Small talk', 'Study together', 'Eating together']
    all_names = context_names+actuator_names
    sensor_len = len(context_names)


    ### Draw Boxplot ###
    fig = plt.figure(figsize=(20, 20))
    axs = list(map(lambda x: fig.add_subplot(sensor_len, 1, x+1), range(sensor_len)))
    

    for i, ax in enumerate(axs):
        sns_ax = sns.boxplot(data=sensor_values[all_names.index(context_names[i])], ax=ax, palette="Set3")
        sns_ax.set_xticklabels(tasks)
        ax.set_ylabel(context_names[i], fontsize = 10, rotation=0, labelpad=15, horizontalalignment='right')
        
    plt.subplots_adjust(left=0.08, bottom=0.02, right=0.98, top=0.98, wspace=None, hspace=0.00)
    plt.show()


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