import pymongo as pm
import datetime
import time
import matplotlib.pyplot as plt
import numpy as np
import sys
import pandas as pd
import json
from utils import *


def publihser_analysis(db_info, start_ts, end_ts):
    ''' Data Crawling from Lapras DB '''
    client = pm.MongoClient(db_info['address'])
    client.data.authenticate(db_info['autheticate']['name'], db_info['autheticate']['pw'], mechanism=db_info['autheticate']['mechanism'])
    db = client.data
    data = db.N1SeminarRoom825_data

    db_datas = [d['publisher'] for d in \
        data.find({'timestamp': {'$gt': start_ts, '$lt': end_ts}}).sort('timestamp')]

    client.close()

    np_datas = np.array(list(set(db_datas)))
    pivot = pd.DataFrame(np_datas, columns=['publisher'])
    fname = 'publihser.xlsx'
    pivot.to_excel(fname,
                    sheet_name='Sheet1',
                    na_rep = 'NaN', 
                    header = True, 
                    index = False, 
            )

def pair_analysis(db_info, start_ts, end_ts):
    ''' Data Crawling from Lapras DB '''
    client = pm.MongoClient(db_info['address'])
    client.data.authenticate(db_info['autheticate']['name'], db_info['autheticate']['pw'], mechanism=db_info['autheticate']['mechanism'])
    db = client.data
    data = db.N1SeminarRoom825_data

    db_datas = [(d['name'], d['publisher']) for d in \
        data.find({'timestamp': {'$gt': start_ts, '$lt': end_ts}}).sort('timestamp')]

    client.close()

    np_datas = np.array(list(set(db_datas)))
    pivot = pd.DataFrame(np_datas, columns=['name', 'publisher'])
    fname = 'pair.xlsx'
    pivot.to_excel(fname,
                    sheet_name='Sheet1',
                    na_rep = 'NaN', 
                    header = True, 
                    index = False, 
            )

def pair_cnt_analysis(db_info, start_ts, end_ts):
    ''' Data Crawling from Lapras DB '''
    client = pm.MongoClient(db_info['address'])
    client.data.authenticate(db_info['autheticate']['name'], db_info['autheticate']['pw'], mechanism=db_info['autheticate']['mechanism'])
    db = client.data
    data = db.N1SeminarRoom825_data

    db_datas = [(d['name'], d['publisher']) for d in \
        data.find({'timestamp': {'$gt': start_ts, '$lt': end_ts}}).sort('timestamp')]

    client.close()

    pairs = list(set(db_datas))
    pair_hash = dict()
    for i in range(len(pairs)):
        pair_hash[pairs[i]] = i 
    
    cnts = np.zeros(len(pairs), dtype=np.int)
    
    for data in db_datas:
        cnts[pair_hash[data]] += 1

    np_datas = np.array(list(map(lambda x, y: (x[0], x[1], y), pairs, cnts)))
    pivot = pd.DataFrame(np_datas, columns=['name', 'publisher', 'count'])
    fname = 'pair_15_17.xlsx'
    pivot.to_excel(fname,
                    sheet_name='Sheet1',
                    na_rep = 'NaN', 
                    header = True, 
                    index = False, 
            )

if __name__ == '__main__':
    start_ts = int(time.mktime(datetime.datetime(2015, 1, 1, 0, 0).timetuple())*1000)
    end_ts = int(time.mktime(datetime.datetime(2017, 1, 1, 0, 0).timetuple())*1000)

    json_file = 'db_info.json'
    with open(json_file, 'r') as f:
        db_info = json.load(f)

    pair_cnt_analysis(db_info, start_ts, end_ts)