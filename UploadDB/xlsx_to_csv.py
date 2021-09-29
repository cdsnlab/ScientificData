import glob
import pandas as pd


def xlsx_to_csv(fnames):
    for fname in fnames:
        df = pd.read_excel(fname)
        new_name = fname.replace('xlsx', 'csv')
        df[['timestamp', 'sensor_name', 'value']].to_csv(new_name, index=None)

if __name__ == '__main__':
    fnames = glob.glob('seminar_modified/*')
    print(fnames)
    xlsx_to_csv(fnames)