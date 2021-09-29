import os
import sys
import json
import glob
import time
import shutil
import paramiko 
from scp import SCPClient, SCPException 
from datetime import date, datetime, timedelta

VIDEO_PATH = 'C:/Users/cdsn/AppData/LocalLow/RecordFiles'
ADDITIONAL_FOLDER = 'HSL-492955-SZWHZ'

class SSHManager: 
    def __init__(self): 
        self.ssh_client = None 
         
    def create_ssh_client(self, host, port, username, password): 
        """Create SSH client session to remote server""" 
        if self.ssh_client is None: 
            self.ssh_client = paramiko.SSHClient() 
            self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy()) 
            self.ssh_client.connect(host, port, username=username, password=password) 
        else: 
            print("SSH client session exist.") 
    
    def close_ssh_client(self): 
        """Close SSH client session""" 
        self.ssh_client.close() 
        
    def send_file(self, local_path, remote_path): 
        """Send a single file to remote path""" 
        try: 
            with SCPClient(self.ssh_client.get_transport()) as scp: 
                scp.put(local_path, remote_path, preserve_times=True) 
        except SCPException: 
            raise SCPException.message 
    
    def send_command(self, command): 
        """Send a single command""" 
        stdout = self.ssh_client.exec_command(command)
        return stdout

def dateChecker():
    today = date.today()
    yesterday = today - timedelta(days=1)
    d_to_s = lambda x: str(x).replace('-', '')
    return d_to_s(today), d_to_s(yesterday)

def fileChecker(day):
    file_list = glob.glob(f'{VIDEO_PATH}/{day}/{ADDITIONAL_FOLDER}/*')
    return file_list

def fileSelector(tfiles, yfiles, prev_tfiles, prev_yfiles):
    today_selected = [x for x in tfiles if x not in prev_tfiles]
    yesterday_selected = [x for x in yfiles if x not in prev_yfiles]
    return today_selected, yesterday_selected


def fileUploader(nas_info, dir, selected, date):
    ip = nas_info['ip']
    port = nas_info['port']
    id = nas_info['id']
    pw = nas_info['pw']
    nas_dir = nas_info[dir]

    ''' SSH connection '''
    ssh_manager = SSHManager() 
    ssh_manager.create_ssh_client(ip, port, id, pw)  

    ''' Make video directory '''
    ssh_manager.send_command(f'mkdir -p {nas_dir}/{date}/{ADDITIONAL_FOLDER}')

    time.sleep(30)

    ''' Send the video '''
    for file in selected:
        ssh_manager.send_file(file, f'{nas_dir}/{date}/{ADDITIONAL_FOLDER}')
    
    ''' Close the connection '''
    ssh_manager.close_ssh_client() 

def webcamDataToNASDay(nas_info, dir):
    prev_today = None
    day_changed = False
    while True:
        ''' Find today '''
        today, yesterday = dateChecker()
        print(f'Now: {datetime.now()} Today: {today}, Yesterday: {yesterday}')
        if prev_today != None:
            if today != prev_today:
                print('day changed')
                day_changed = True
        if day_changed:
            ''' Find all video files created within today and yesterday '''
            tfiles, yfiles = fileChecker(today), fileChecker(yesterday)
            print(f'Today\'s file: {tfiles}')
            if len(tfiles) > 0:
                print(f'Upload videos collected on {yesterday}')
                fail_cnt = 0
                while fail_cnt < 6:
                    try:
                        fileUploader(nas_info, dir, yfiles, yesterday)
                        deleteOldDays()
                        day_changed = False
                        break
                    except Exception as e:
                        print(f'Exception occur\n---------------------\n{e}')
                        fail_cnt += 1
                        time.sleep(600)
                if fail_cnt >= 6:
                    raise Exception('Upload Error occur')
            

        print('\n--------------------------\n')
        prev_today = today
        time.sleep(3600*3)

def uploadDays(nas_info, dir, day_list):
    for day in day_list:
        print(day)
        files = fileChecker(day)
        print(files)
        fileUploader(nas_info, dir, files, day)

def deleteOldDays():
    day_list = sorted(os.listdir(VIDEO_PATH))
    while len(day_list) > 3:
        day = day_list.pop(0)
        print(f'Remove : {day}')
        shutil.rmtree(f'{VIDEO_PATH}/{day}')
    print(f'Remain {day_list}')

if __name__ == '__main__':
    # dir = 'SEMINAR_DIR'
    dir = 'LOUNGE_DIR'
    json_file = 'nas_info.json'
    with open(json_file, 'r') as f:
        nas_info = json.load(f)
        f.close()

    mode = input('select the mode (0: quit, 1: webcamDataToNASDay, 2: uploadDays) ')
    while not mode in ['0', '1', '2']:
        print('wrong input')
        mode = input('select the mode (0: quit, 1: webcamDataToNASDay, 2: uploadDays) ')

    if mode == '0':
        sys.exit()
    elif mode == '1':
        webcamDataToNASDay(nas_info, dir)
    elif mode == '2':
        with open('day_list.txt', 'r') as f:
            day_list = f.readlines()
            f.close()
        day_list = list(map(lambda x: x.strip(), day_list))
        uploadDays(nas_info, dir, day_list)
    else:
        print('Do not come here')
        sys.exit()

