import datetime
import pandas as pd


def revise_time(anchdor_time, minute, second):
    anchor_dt = datetime.datetime(1, 1, 1, anchdor_time.hour, anchdor_time.minute, anchdor_time.second)
    delta = datetime.timedelta(minutes=minute, seconds=second)
    revised_dt = anchor_dt + delta
    revised_time = revised_dt.time()
    return revised_time

def correct_time(anchor_fname, label_fname):
    ''' Anchor dictionary '''
    anchor_file = pd.read_excel(anchor_fname, sheet_name='Sheet1', header=None)
    label_file = pd.read_excel(label_fname, sheet_name=['17.11.', '17.12.'], header=0)
    fnames = anchor_file[0].tolist()
    anchors = anchor_file[1].tolist()
    pairs = tuple(map(lambda x, y: (x, y), fnames, anchors))
    anchor_dict = dict(pairs)
    
    label_file['17.11.'].fillna('', inplace=True)
    label_file['17.12.'].fillna('', inplace=True)

    # print(len(label_file['17.11.']))

    for sheet_name, df in label_file.items():
        print(sheet_name)
        start_times = []
        end_times = []
        for i in range(len(df)):
            video_names = df['파일명'][i].split(',')
            video_names = list(map(lambda x: x.strip(), video_names))
            
            start_time = df['시작시간'][i]
            end_time = df['종료시간'][i]

            correct_start_time = revise_time(anchor_dict[video_names[0]], start_time.minute, start_time.second)
            correct_end_time = revise_time(anchor_dict[video_names[-1]], end_time.minute, end_time.second)

            start_times.append(correct_start_time)
            end_times.append(correct_end_time)


        result = list(map(lambda x, y: f'{str(x)}, {str(y)}', start_times, end_times))
        with open(sheet_name.replace('.', '_')+'corrected.csv', 'w') as f:
            for x in result:
                f.write(f'{x}\n')
            f.close()




if __name__ == '__main__':
    anchor_fname = 'file_to_time.xlsx'
    label_fname = 'SeminarRoom_Labeling.xlsx'

    correct_time(anchor_fname, label_fname)