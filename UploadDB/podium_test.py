import os
import sys
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


FPATH = '/home/skygun/Dropbox/CDSN/Testbed/ScientificData/Code/ScientificData/UploadDB/DOO-RE/Seminar/sensor/Seminar_0.csv'

if __name__ == "__main__":

    epi_df = pd.read_csv(FPATH, )

    podium = epi_df[epi_df.sensor_name == "PodiumIR"]
    # podium['value'].astype(float) 
    podium['value'] = pd.to_numeric(podium['value'])
    podium['timestamp'] = pd.to_datetime(podium['timestamp'])
    print(podium.dtypes)

    # podium.loc[:, 'value'] = podium.loc[:, 'value'].copy().apply(lambda x: 2.076/(x/1000 - 0.011))


    sns.lineplot(
        data=podium, 
        x="timestamp", 
        y="value"

    )
    plt.show()
