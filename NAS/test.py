import os
import sys
import json
import glob
import time
import shutil
import paramiko 
from scp import SCPClient, SCPException 
from datetime import date, datetime, timedelta

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
        _, stdout, _ = self.ssh_client.exec_command(command)
        return stdout


def get_uploaded_dates(nas_info, dir):
    ip = nas_info['ip']
    port = nas_info['port']
    id = nas_info['id']
    pw = nas_info['pw']
    nas_dir = nas_info[dir]

    ''' SSH connection '''
    ssh_manager = SSHManager() 
    ssh_manager.create_ssh_client(ip, port, id, pw)  

    ''' Make video directory '''
    stdout = ssh_manager.send_command(f'ls -bd {nas_dir}/*')
    uploaded_list = stdout.readlines()
    uploaded_list = list(map(lambda x: x.split('/')[-1].strip(), uploaded_list))

    ''' Close the connection '''
    ssh_manager.close_ssh_client() 
    return uploaded_list

def upload_remains(nas_info, dir):
    dir = 'SEMINAR_DIR'
    json_file = 'nas_info.json'
    with open(json_file, 'r') as f:
        nas_info = json.load(f)
        f.close()
    uploaded_list = get_uploaded_dates(nas_info, dir)
    today = '20211109'
    date_list = ['20211105', '20211106', '20211107', '20211108', '20211109']
    print(date_list)
    if today in date_list:
        date_list.remove(today)
    print(date_list)

    uploaded_list = list(filter(lambda x: x>=date_list[0], uploaded_list))
    print('uploaded_list:', uploaded_list)

    to_be_deleted = list(filter(lambda x: x in uploaded_list, date_list))
    to_be_uploaed = list(filter(lambda x: x not in uploaded_list, date_list))


if __name__ == '__main__':
    dir = 'SEMINAR_DIR'
    json_file = 'nas_info.json'
    with open(json_file, 'r') as f:
        nas_info = json.load(f)
        f.close()
    upload_remains(nas_info, dir)