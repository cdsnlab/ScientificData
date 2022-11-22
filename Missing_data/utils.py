import datetime
import time
from dateutil.relativedelta import relativedelta

def roundup(x, scale):
    return x if x % scale == 0 else x + scale - x % scale

def rounddown(x, scale):
    return x if x % scale == 0 else (x // scale) * scale

def to_day(x):
    x_dt = datetime.datetime.fromtimestamp(x/1000)
    only_day =  x_dt.replace(hour=0, minute=0, second=0, microsecond=0)
    return int(time.mktime(only_day.timetuple())*1000)

def ts_to_dt(timestamp):
    return datetime.datetime.fromtimestamp(timestamp/1000).strftime('%y/%m/%d')

def create_datetick(start_ts, end_ts, scale='month', add=1):
    start_dt = datetime.datetime.fromtimestamp(start_ts/1000)
    end_dt = datetime.datetime.fromtimestamp(end_ts/1000)
    dts = [start_dt]
    next_dt = add_datetime(start_dt, scale, add)
    while next_dt <= end_dt:
        dts.append(next_dt)
        next_dt = add_datetime(next_dt, scale, add)
    result = list(map(lambda x: x.strftime('%y/%m/%d'), dts))
    return result

def add_datetime(dt, scale='month', add=1):
    if scale == 'min':
        next_dt = dt + relativedelta(minutes=add)
    elif scale == 'hour':
        next_dt = dt + relativedelta(hours=add)
    elif scale == 'day':
        next_dt = dt + relativedelta(days=add)
    elif scale == 'week':
        next_dt = dt + relativedelta(weeks=add)
    elif scale == 'month':
        next_dt = dt + relativedelta(months=add)
    elif scale == 'year':
        next_dt = dt + relativedelta(year=add)
    else: 
        return False
    return next_dt

def load_sensor_list():
    with open('agent_list.txt', 'r') as f:
        sensor_list = f.readlines()
        sensor_list = list(map(lambda x: x.strip(), sensor_list))
        f.close()
    return sensor_list

def load_context_list():
    with open('context_list.txt', 'r') as f:
        sensor_list = f.readlines()
        sensor_list = list(map(lambda x: x.strip(), sensor_list))
        f.close()
    return sensor_list

def load_publisher_list():
    with open('all_publisher.txt', 'r') as f:
        sensor_list = f.readlines()
        sensor_list = list(map(lambda x: x.strip(), sensor_list))
        f.close()
    return sensor_list

def load_list(path):
    with open(path, 'r') as f:
        sensor_list = f.readlines()
        sensor_list = list(map(lambda x: x.strip(), sensor_list))
        f.close()
    return sensor_list