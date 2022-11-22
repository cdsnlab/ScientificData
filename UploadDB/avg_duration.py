import os 
import glob

def avg_duration(path):
    metas = glob.glob(f'{path}/*')
    durations = []
    for meta in metas:
        with open(meta, 'r') as f:
            texts = f.readlines()
            durations.append(int(texts[4].strip().split(' ')[-1]))
    # print(durations)
    # under_5min = list(filter(lambda x: x < 60*5, durations))
    # print(len(under_5min))
    # print(under_5min)
    return sum(durations)/len(durations)

def activities_duration(activities):
    for activity in activities:
        duration = avg_duration(f'ScientificData/{activity}/metadata')
        print(activity + ',' + str(duration))

if __name__ == '__main__':
    # path = 'metadata'
    # avg_duration(path)
    activities = os.listdir('ScientificData')
    activities_duration(activities)