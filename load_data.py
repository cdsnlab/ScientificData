from pymongo import MongoClient
import sys
import pickle
import json

with open("./keys/config_mongo.json") as f:
    info=json.load(f)

username=info['username']
password=info['password']

try:
    conn=MongoClient('smart-iot.kaist.ac.kr', 
                        username=username,
                        password=password,
                        authSource='data',
                        authMechanism='SCRAM-SHA-1')
    db=conn.data
    collection=db.N1SeminarRoom825_data
    print("Connection success.")
except:
    print("Connection error.")
    sys.exit()

query={"$or":[ {"publisher": "SeatAgent"}, {"publisher": "MonnitServerAgent"}]}
# query={"name": "Aircon1"}
monnit_data=collection.find(query) #TODO

data=[]
for datum in monnit_data:
    data.append(datum)
print(len(data))
with open("./dataset/mongoDB/data_db.pkl", "wb") as f:
    pickle.dump(data, f)

