import glob
import pandas as pd

def data_cleaning(fnames):
    for fname in fnames:
        df = pd.read_csv(fname)
        df.iloc[:, 0:3].to_csv(fname, index=None)


if __name__ == '__main__':
    fnames = glob.glob('sensor/*')
    data_cleaning(fnames)