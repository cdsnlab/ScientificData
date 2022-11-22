from re import L
import json
import lxml
import sys
import re
import time
import json
from bs4 import BeautifulSoup as bs
# from utils import logger
# from utils import datetostamp as dts
from pymongo import MongoClient
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

with open("./keys/config_mongo.json") as f:
    info_mongo=json.load(f)

username_mongo=info_mongo['username']
password_mongo=info_mongo['password']

with open("./keys/config_imonnit.json") as f:
    info_imonnit=json.load(f)

username_imonnit=info_imonnit['username']
password_imonnit=info_imonnit['password']

# make logger
# logger=logger.make_logger()

# create Session
def create_session():
    chrome_options=Options() # define browser options
    chrome_options.binary_location=''
    chrome_options.add_argument('--headless') # hide the browser window
    chrome_path=r'/usr/local/bin/chromedriver'
    # driver=webdriver.Chrome(executable_path=chrome_path, options=chrome_options)
    driver=webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    return driver

def login_and_links(s: webdriver.Chrome):
    s.get('https://www.imonnit.com')
    # s.find_element_by_id('UserName').send_keys(username_imonnit)
    # s.find_element_by_id('Password').send_keys(password_imonnit)
    # s.find_element_by_xpath("//input[@value='Login']").click()
    s.find_element(By.ID, 'UserName').send_keys(username_imonnit)
    s.find_element(By.ID, 'Password').send_keys(password_imonnit)
    s.find_element(By.XPATH, "//input[@value='Login']").click()
    
    soup=bs(s.page_source,'lxml')
    # print(soup)
    # get page list of all sensors (21 sensors)
    value=soup.findAll(href=re.compile("^/Overview/SensorChart"), style=re.compile('^color:'))
    # print(value)
    href_list=['https://www.imonnit.com'+(item['href'].replace('Chart',"Home")) for i, item in enumerate(value) if i%2==0]
    
    return href_list

##########################################################################
# connection to MongoDB, data collection, test table

try:
    conn=MongoClient('smart-iot.kaist.ac.kr', 
                        username=username_mongo,
                        password=password_mongo,
                        authSource='data',
                        authMechanism='SCRAM-SHA-1')
    # logger.debug('MongoDB: Successfully Connected.')
    print("mongoDB: connected.")
    db=conn.data
    collection=db.test
except:
    print("mongoDB: connection failed.")
    # logger.error('MongoDB: Fail to connect.')
    sys.exit()

##########################################################################

# load sensor_dict from latest_timestamp.json
# with open('latest_timestamp.json','r') as f:
#     sensor_dict=json.load(f)

with create_session() as s:
    if s==None:
        # logger.error('Fail to create session.')
        print("selenium: ERROR in create_session")
        sys.exit()
    print("selenium: session created.")
    href_list=login_and_links(s)
    print(href_list)
    for i, url in enumerate(href_list):
        doc=[]
        s.get(url)
        time.sleep(2) # wait javascript function loading for displaying sensor data
        soup=bs(s.page_source, 'lxml')

        # get the name of sensor
        value=soup.find('span',{"style":'font-size: 14px; font-weight: 500;'})
        sensor_name=value.contents[0] # name, publisher
        # logger.debug('SENSOR {}'.format(sensor_name))

        # get the value of sensor
        value=soup.find_all('div', class_='col-xs-5 col-md-5 col-sm-5 historyReading')
        pr_list=[item.contents[0] for item in value] # value
        pr_list.reverse() # follow the temporal order in case of having multiple values in same timestamp

        # get the timestamp of each value
        value=soup.find_all('div', class_='col-xs-4 col-md-4 col-sm-4 historyDate')
        for j, item in enumerate(value):
            print(value.contents[0])
        # tm_list=[dts.date_to_tstamp(item.contents[0]) for i, item in enumerate(value)] # timestamp
        # tm_list.reverse() # follow the temporal order in case of having multiple values in same timestamp

        # for t, item in enumerate(pr_list):
        #     # if crawled date is before the latest crawled date, then continue
        #     # if tm_list[t]<int(sensor_dict[sensor_name]):
        #     #     continue

        #     # logger.debug('{}, {}'.format(datetime.fromtimestamp(tm_list[t]), item))
        #     rec={   'type':     'context', 
        #             'name':     sensor_name, 
        #             'value':    item, 
        #             'timestamp':tm_list[t],
        #             'publisher':sensor_name}
        #     doc.append(rec)

        # # update to the latest time
        # sensor_dict[sensor_name]=max(tm_list)

        # # insert all gathered data from one sensor
        # try:
        #     result=collection.insert(doc)
        # except:
        #     logger.error('{}th, {}'.format(i+1, sensor_name))

    # ## save the latest time to avoid duplicated crawling
    # with open('latest_timestamp.json','w') as f:
    #     json.dump(sensor_dict, f)
