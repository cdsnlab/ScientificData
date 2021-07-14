import os
import json
import glob
import time
import shutil
import paramiko 
from scp import SCPClient, SCPException 
from datetime import date, datetime, timedelta

VIDEO_PATH = 'C:/Users/cdsn/RecordFiles'
ADDITIONAL_FOLDER = 'HSL-492641-GLULE'

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

def webcamDataToNASInstant(nas_info, dir):
    prev_today = None
    prev_tfiles, prev_yfiles = None, None
    while True:
        ''' Find today '''
        today, yesterday = dateChecker()
        print(f'Now: {datetime.now()} Today: {today}, Yesterday: {yesterday}')
        if prev_today != None:
            if prev_today != today:
                prev_tfiles, prev_yfiles = [], tfiles

        ''' Find all video files created within today and yesterday '''
        tfiles, yfiles = fileChecker(today), fileChecker(yesterday)
        tfiles = tfiles[:-1]
        if prev_tfiles != None:
            ''' Select the file to be uploaded'''
            today_selected, yesterday_selected = fileSelector(tfiles, yfiles, prev_tfiles, prev_yfiles)
            print(f'selected:\n{today_selected, yesterday_selected}')

            fileUploader(nas_info, dir, today_selected, today)
            fileUploader(nas_info, dir, yesterday_selected, yesterday)
        print('\n--------------------------\n')
        prev_tfiles, prev_yfiles = tfiles, yfiles
        prev_today = today
        time.sleep(300)

def webcamDataToNASDay(nas_info, dir):
    prev_today = None
    day_changed = False
    while True:
        ''' Find today '''
        today, yesterday = dateChecker()
        print(f'Now: {datetime.now()} Today: {today}, Yesterday: {yesterday}')
        if prev_today != None:
            if today != prev_today:
                day_changed = True
        if day_changed:
            ''' Find all video files created within today and yesterday '''
            tfiles, yfiles = fileChecker(today), fileChecker(yesterday)
            if len(tfiles) > 0:
                print(f'Upload videos collected on {yesterday}')
                fileUploader(nas_info, dir, yfiles, yesterday)
                deleteOldDays()
                day_changed = False
            

        print('\n--------------------------\n')
        prev_today = today
        time.sleep(3600*3)

def uploadDays(nas_info, dir, day_list):
    for day in day_list:
        print(day)
        files = fileChecker(day)
        fileUploader(nas_info, dir, files, day)

def deleteOldDays():
    day_list = sorted(os.listdir(VIDEO_PATH))
    while len(day_list) > 3:
        day = day_list.pop(0)
        print(f'Remove : {day}')
        shutil.rmtree(f'{VIDEO_PATH}/{day}')
    print(f'Remain {day_list}')

if __name__ == '__main__':
    dir = 'SEMINAR_DIR'
    # dir = 'LOUNGE_DIR'
    json_file = 'C:/Users/CDSN Lab/Desktop/nas_info.json'
    with open(json_file, 'r') as f:
        nas_info = json.load(f)

    # webcamDataToNASInstant(nas_info, dir)
    webcamDataToNASDay(nas_info, dir)
    day_list = ['20210625', '20210626', '20210627']
    # uploadDays(nas_info, dir, day_list)

