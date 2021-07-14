import datetime
import pandas as pd
import matplotlib.pyplot as plt
import glob
import seaborn as sns
import sys

def draw_value(data_file, fname):
    data = pd.read_csv(data_file)
    plt.plot(data['timestamp'], data['value'])

    # plt.legend(fontsize=5, loc='upper right')
    plt.xlabel('timestamp')
    plt.ylabel('value')
    plt.show()
    # plt.savefig(fname, dpi = 1000)
    # plt.clf()

if __name__ == '__main__':
    fname = 'sound_test.png'
    data_file = 'query/SoundWall1.csv'
    draw_value(data_file, fname)
