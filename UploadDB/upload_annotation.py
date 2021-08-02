import sys
import time
import json
import datetime
import pymongo as pm
import pandas as pd


def upload_annotation(db_info, label_fname):
    ''' Connect DB '''
    label_file = pd.read_excel(label_fname, sheet_name=['17.09.', '17.10.', '17.11.', '17.12.'], header=0)
    label_file['17.09.'].fillna('', inplace=True)
    label_file['17.10.'].fillna('', inplace=True)
    label_file['17.11.'].fillna('', inplace=True)
    label_file['17.12.'].fillna('', inplace=True)

    client = pm.MongoClient(db_info['address'])
    client.data.authenticate(db_info['autheticate']['name'], db_info['autheticate']['pw'], mechanism=db_info['autheticate']['mechanism'])
    db = client.data
    data = db.N1SeminarRoom825_Annotation

    for sheet_name, df in label_file.items():
        print(sheet_name)
        label_col2 = '기수'
        label_col3 = '건' if '건' in df.columns else '태훈'
        for i in range(len(df)):
            ''' Data Extraction '''
            if df['날짜'][i] == '':
                break
            date = str(int(df['날짜'][i]))
            files = df['파일명'][i]
            start_time = str(df['시작시간'][i])
            end_time = str(df['종료시간'][i])
            label = df['레이블'][i]
            label2, label3 = df[label_col2][i], df[label_col3][i]
            human_cnt = str(df['사람 수'][i])
            # print(date, files, start_time, end_time, label, human_cnt)

            ''' Data Processing 1 - timestamp '''
            y, m, d = int(date[:4]), int(date[4:6]), int(date[6:8])
            start_time_list = list(map(lambda x: int(x), start_time.split(':')))
            end_time_list = list(map(lambda x: int(x), end_time.split(':')))

            start_dt = datetime.datetime(y, m, d, start_time_list[0], start_time_list[1], start_time_list[2])
            end_dt = datetime.datetime(y, m, d, end_time_list[0], end_time_list[1], end_time_list[2])
            if end_dt < start_dt:
                end_dt = end_dt + datetime.timedelta(days=1) # when Activity continue next day

            start_ts = int(time.mktime(start_dt.timetuple())*1000)
            end_ts = int(time.mktime(end_dt.timetuple())*1000)
            duration = end_ts - start_ts

            ''' Data Processing 2 - avg number of humans, label matching '''
            human_cnts = list(map(lambda x: int(x), human_cnt.split('~')))
            avg_n_human = sum(human_cnts)/len(human_cnts)
            matched = label == label2 == label3
            
            ''' Upload Data document '''
            data.insert_one({'date': date, 
                        'video_names': files, 
                        'start_timestamp': start_ts, 
                        'end_timestamp': end_ts, 
                        'label': label, 
                        'matched': matched,
                        'duration': duration, 
                        'avg_n_human': avg_n_human})
        break
    client.close()

if __name__ == '__main__':
    label_fname = 'SeminarRoom_Labeling.xlsx' # Excel file which is downloaded version of google spread sheet 'SeminarRoom_Labeling'
    json_file = 'db_info.json'
    with open(json_file, 'r') as f:
        db_info = json.load(f)
    
    upload_annotation(db_info, label_fname)
