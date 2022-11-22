import json
import requests


RETRIEVE_API = 'webapi/query.cgi?api=SYNO.API.Info&version=1&method=query&query=SYNO.API.Auth,SYNO.FileStation'
LOGIN_API = 'webapi/auth.cgi?api=SYNO.API.Auth&version=3&method=login&account={}&passwd={}&session=FileStation&format=cookie'
LOGOUT_API = 'webapi/auth.cgi?api=SYNO.API.Auth&version=1&method=logout&session=FileStation'
LS_API = 'webapi/entry.cgi?api=SYNO.FileStation.List&version=2&method=list&additional=&folder_path={}&_sid={}'
MKDIR_API = 'webapi/entry.cgi?api=SYNO.FileStation.CreateFolder&version=2&method=create&folder_path={}&name={}&_sid={}'
UPLOAD_API = 'webapi/entry.cgi?&_sid={}'


def retreive(url):
    success = False
    response = requests.get(url+RETRIEVE_API)
    code = response.status_code
    response_dict = response.json()
    success = response_dict['success']
    return code, success

def login(url, id, pw):
    success, sid = False, 0
    response = requests.get(url+LOGIN_API.format(id, pw))
    code = response.status_code
    response_dict = response.json()
    success = response_dict['success']
    sid = response_dict['data']['sid']
    return code, success, sid

def logout(url):
    success = False
    response = requests.get(url+LOGOUT_API)
    code = response.status_code
    response_dict = response.json()
    success = response_dict['success']
    return code, success

def ls(url, sid, path):
    success, filelist = False, dict()
    response = requests.get(url+LS_API.format(path, sid))
    code = response.status_code
    response_dict = response.json()
    success = response_dict['success']
    filelist = response_dict['data']['files']
    return code, success, filelist

def mkdir(url, sid, path, name):
    success = False
    response = requests.get(url+MKDIR_API.format(path, name, sid))
    code = response.status_code
    response_dict = response.json()
    success = response_dict['success']
    return code, success

def upload(url, sid, path, filepath):
    success = False
    content_disposition = {'api': 'SYNO.FileStation.Upload', 'version': '2', 'method': 'upload', 'path': path, 'create_parents': 'true'}
    response = requests.post(url+UPLOAD_API.format(sid), 
                            files={'file': open(filepath, 'rb')},
                            data=content_disposition
                            )
    code = response.status_code
    response_dict = response.json()
    success = response_dict['success']
    return code, success



if __name__ == '__main__':
    test_file = 'C:/Users/cdsnlab/Dropbox/CDSN/Testbed/NAS/3. URP Report_example.jpg'
    seminar_dir = '/volume1/N1SeminarRoom825'
    json_file = 'old_nas_info.json'
    with open(json_file, 'r') as f:
        nas_info = json.load(f)
    URL = nas_info['url']
    ID = nas_info['admin']
    PW = nas_info['pw']

    code, success = retreive(URL)
    code, success, sid = login(URL, ID, PW)
    code, success, filelist = ls(URL, sid, seminar_dir)
    code, success = mkdir(URL, sid, path=seminar_dir, name='test')
    code, success = upload(URL, sid, path=seminar_dir, filepath=test_file)
    code, success = logout(URL)


    
