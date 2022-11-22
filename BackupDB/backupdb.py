import sys
import time
import json
import glob
import shutil
import paramiko
import datetime
import subprocess
from scp import SCPClient, SCPException 


with open('command.txt') as f:
    COMMAND = f.read()
    f.close()
DEST = './dump'
COLLECTIONS = ['N1SeminarRoom825_data', 'N1Lounge8F_data']

class SSHManager: 
    def __init__(self): 
        self.ssh_client = None 
         
    def create_ssh_client(self, host, port, username, password): 
        """Create SSH client session to remote server""" 
        if self.ssh_client is None: 
            self.ssh_client = paramiko.SSHClient() 
            self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy()) 
            self.ssh_client.connect(host, port, username=username, password=password, banner_timeout=200) 
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
        _, stdout, _ = self.ssh_client.exec_command(command)
        return stdout

def fileUploader(nas_info, dir, date):
    ip = nas_info['ip']
    port = nas_info['port']
    id = nas_info['id']
    pw = nas_info['pw']
    nas_dir = nas_info[dir]

    ''' SSH connection '''
    ssh_manager = SSHManager() 
    ssh_manager.create_ssh_client(ip, port, id, pw)  

    ''' Make video directory '''
    ssh_manager.send_command(f'mkdir -p {nas_dir}/{date}')

    time.sleep(30)

    ''' Send the video '''
    selected = glob.glob(f'{DEST}/data/*')

    for file in selected:
        ssh_manager.send_file(file, f'{nas_dir}/{date}')
    
    ''' Close the connection '''
    ssh_manager.close_ssh_client() 

def backup_to_local(coverage='essential'):
    if coverage == 'all':
        command = COMMAND.split(' ')[:-2]
        subprocess.run(command, stdout=subprocess.PIPE)
    elif coverage == 'essential':
        for collection in COLLECTIONS:
            command = COMMAND.format(collection)
            command = command.split(' ')
            subprocess.run(command, stdout=subprocess.PIPE)

def delete_local():
    shutil.rmtree(DEST)

def backup_schedule(nas_info, day_interval):
    prev = None
    dir = 'BACKUP_ESSENTIAL_DIR'
    while True:
        today = datetime.datetime.now()
        
        if prev == None or (today - prev).days >= day_interval:
            backup_to_local('essential')
            date = today.strftime("%Y%m%d")

            fileUploader(nas_info, dir, date)
            delete_local()
            prev = today

        # time.sleep(1)
        time.sleep(60*60*24)

def backup_all(nas_info):
    today = datetime.datetime.now()
    backup_to_local('all')
    date = today.strftime("%Y%m%d")
    dir = 'BACKUP_ALL_DIR'
    fileUploader(nas_info, dir, date)
    delete_local()


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('need more argument')
        sys.exit()

    print(sys.argv)
    json_file = 'nas_info.json'
    with open(json_file, 'r') as f:
        nas_info = json.load(f)
        f.close()
    
    if sys.argv[1] == 'all':
        backup_all(nas_info)
    
    elif sys.argv[1] == 'essential':
        day_interval = 7
        backup_schedule(nas_info, day_interval)


