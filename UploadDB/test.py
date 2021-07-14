import datetime
import pandas as pd

# t1 = datetime.datetime(2017, 11, 1, 11, 35, 37)
# t2 = datetime.datetime(2017, 11, 1, 11, 38, 12)

# delta = t2 - t1
# print(delta)

def revise_time(anchdor_time, minute, second):
    anchor_dt = datetime.datetime(1, 1, 1, anchdor_time.hour, anchdor_time.minute, anchdor_time.second)
    delta = datetime.timedelta(minutes=minute, seconds=second)
    revised_dt = anchor_dt + delta
    revised_time = revised_dt.time()
    return revised_time

time_file = pd.read_excel('file_to_time.xlsx', sheet_name='Sheet1', header=None)

print(time_file)


sample = time_file[1][2]

print(sample)
print(type(sample))
sample_dt = datetime.datetime(1, 1, 1, sample.hour, sample.minute, sample.second)
t2 = datetime.timedelta(minutes=21, seconds=30)
new_dt = sample_dt + t2
new_time = new_dt.time()

print(new_time)

fnames = time_file[0].tolist()
anchors = time_file[1].tolist()

pairs = tuple(map(lambda x, y: (x, y), fnames, anchors))
pair_dict = dict(pairs)


for key, value in pair_dict.items():
    print(key, value)


