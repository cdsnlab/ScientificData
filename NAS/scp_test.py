import paramiko 
from scp import SCPClient, SCPException 

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
        return stdout.readlines()





IP = '143.248.53.238'
PORT = 7759
ID = 'admin'
PW = 'CdsnLab@7759'

test_file = 'C:/Users/cdsnlab/Dropbox/CDSN/Testbed/NAS/3. URP Report_example.jpg'
seminar_dir = '/volume1/N1SeminarRoom825/'
new_dir = 'new'

ssh_manager = SSHManager() 
ssh_manager.create_ssh_client(IP, PORT, ID, PW)  
ssh_manager.send_command(f'mkdir {seminar_dir}/{new_dir}')
ssh_manager.send_file(test_file, f'{seminar_dir}/{new_dir}')  
ssh_manager.close_ssh_client() # 세션종료


