import sys
import time
import json
import datetime
import pymongo as pm
import pandas as pd

def test_upload(db_info):
    client = pm.MongoClient(db_info['address'])
    client.data.authenticate(db_info['autheticate']['name'], db_info['autheticate']['pw'], mechanism=db_info['autheticate']['mechanism'])
    db = client.data
    data = db.Lapras_Test

    data.insert_one({   'type': 'functionality',
                        'publisher': 'GEON',
                        'name': 'geontest', 
                        'timestamp': int(time.time()*1000), 
                        'arguments': ['a', 'b', 'c']})

    client.close()

if __name__ == '__main__':
    json_file = 'info/db_info.json'
    with open(json_file, 'r') as f:
        db_info = json.load(f)

    test_upload(db_info)