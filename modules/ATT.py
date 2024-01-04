#%%
import os
from time import time, sleep
from os.path import dirname, join, basename
import requests 
import mimetypes
import string
from requests_toolbelt.multipart.encoder import MultipartEncoder
from random import choice, randint, choices

class ATAPI:
    def __init__(self, host, port = 8080):
        self.host = host
        self.port = port
        self._api = f'http://{self.host}:{self.port}'

    def get_running(self):
        res_json = requests.get(self._api + '/runningScripts').json()
        return res_json
    
    def run_code(self, path):
        for i in range(3):
            params = {
                'path': path,
            }
            res_json = requests.get(self._api + '/control/start_playing', params=params).json()
            return res_json.get('status') == 'success'
    
    def stop_run(self, path):
        for i in range(5):
            params = {
                'path': path,
            }
            res_json = requests.get(self._api + '/control/stop_playing', params=params).json()
            if res_json.get('status') == 'success':
                for i in range(100):
                    running_paths = self.get_running()
                    if path not in running_paths:
                        return True
                    else:
                        sleep(.5)
            return False
    def create_folder(self,path):
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
        }

        params = {
            'path': path,
        }
        res_json = requests.get(self._api + '/file/newFolder', params=params, headers=headers, )

    def upload_file(self, path, local_path):
        if self.exist_file(path):
            self.delete_file(path)
        boundary = '----WebKitFormBoundary'+''.join(choices(string.ascii_letters + string.digits, k=16))
        headers = {
            'Content-Type': f'multipart/form-data; boundary={boundary}',
        }

        params = {
            'path': path,
        }
        file_name = basename(local_path)
        multipart_data = MultipartEncoder(
            fields={
                'file': (file_name, open(local_path, 'rb'), mimetypes.guess_type(local_path))
                }, 
            boundary=boundary
        )

        res_json = requests.post(self._api + '/file/upload', params=params, headers=headers, data=multipart_data, verify=False,timeout=5).json()
        return res_json.get('status') == 'success'
    def convert_path(self,path):
        new_path = os.path.normpath(path)
        new_path = new_path.replace("\\", "/")
        return new_path

    def upload_folder(self,path):
        for root, _, files in os.walk(path):
        #create root folder
            new_root = self.convert_path(root)
            self.create_folder(new_root)
            for file in files:
                #Upload folder
                file_path = os.path.join(root, file)
                new_path = self.convert_path(file_path)
                if not self.exist_file(new_path):
                    self.upload_file(new_path,new_path)
        return True
    def update_file(self, path, local_file):
        if self.exist_file(path):
            self.delete_file(path)
        if not os.path.exists(local_file):
            return False
        if not self.exist_file(path):
            return self.upload_file(path, local_file)
        
        try:
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded',
            }

            params = {
                'path': path,
            }
            with open(local_file) as f:
                file_content = f.read()
            data = {
                'content': file_content,
            }
            res_json = requests.post(self._api + '/file/update', params=params, headers=headers, data=data).json()
            return res_json.get('status') == 'success'
        except Exception as e:
            print(f'ERROR:file {self.path} update:', e)
            return False
        
    def exist_file(self, path):
        parent_dir = dirname(path)
        files = self.list_dir(parent_dir)
        # print(files)
        for f in files:
            if path in f.get('filePath'):
                return True
        return False
    
    def delete_file(self, path):
        params = {
            'path': path,
        }
        res_json = requests.get(self._api + '/file/delete', params=params,timeout=3).json()
        return res_json.get('status') == 'success'
    
    def get_file_content(self, path):
        headers = {
            'Accept': 'application/json, text/plain, */*',
        }
        params = {
            'path': path,
        }
        res_json = requests.get(self._api + '/file/content', params=params, headers=headers).json()
        return res_json.get('content') if res_json.get('content') else ''
    def get_log(self):
        headers = {
            'Accept': 'application/json, text/plain, */*',
            }
        res_json = requests.get(self._api + '/log', headers=headers).json()
        return res_json.get('content') if res_json.get('content') else ''
    def list_dir(self, path):
        if not path:
            path = '/'
        path = path.replace('//', '/').replace('\\', '/')
        params = {
            'path': f'{path}',
        }
        res = requests.get(self._api + '/files', params= params, )
        return res.json()['files']
    
    def rename_file(self, path, new_path):
        params = {
            'path': path,
            'newPath': new_path,
        }
        res_json = requests.get(self._api + '/file/rename', params=params, ).json()
        return res_json.get('status') == 'success'
    def clear_log(self):
        res_json = requests.get(self._api + '/log/clear', ).json()
        return res_json


    
# ts = time()
# api = ATAPI('192.168.3.117')
# print(api.get_running())
# local_file = r'E:\py_project\xeon\AutoTouchSync\reg.ate'
# path = '/reg.ate'

# result = api.upload_file(path, local_file)
# print(result)
# print(time() - ts)