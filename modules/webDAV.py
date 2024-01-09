
import json
from webdav3.client import Client
from uuid import uuid4
from os.path import dirname, join
import os
curdir = dirname(__file__)
class ATT_DAV:
    def __init__(self,host:str):
        self.host = host
        self.options = {
        'webdav_hostname': "http://"+self.host,
        'webdav_login':    "root",
        'webdav_password': "alpine",
        'webdav_timeout': 5
        }
        self.client = Client(self.options)
        self.client.verify = False
    def upload_folder(self,local_path,remote_path):
        if not self.client.check(remote_path):
            self.client.mkdir(remote_path)
            self.client.upload_sync(remote_path, local_path)
        else:
            self.client.clean(remote_path)
            self.client.upload_sync(remote_path, local_path)
        return True
    def update_file(self,remote_path, content):
        path_temp = join(curdir, 'Temp')
        file_temp = join(path_temp,str(uuid4())+'.json')
        print(file_temp)
        json_object = json.dumps(content, indent=4)
        with open(file_temp, "w+") as outfile:
            outfile.write(json_object)
             
        if self.client.check(remote_path):
            self.client.clean(remote_path)
        if not self.client.check(remote_path):
            self.client.upload_sync(remote_path, file_temp)
            os.remove(file_temp)
            return True
        self.client.upload_sync(remote_path,local_path=file_temp)
        os.remove(file_temp)
        return True
    def rename_file(self,remote_path,new_name):
        res = self.client.resource(remote_path)
        res.rename(new_name)
        return True
    # def delete_folder(self,remote_path):
    #     return self.client.clean(remote_path)

# app = ATT_DAV("192.168.3.101")
# content = {
#     "proxyHost": "192.168.3.3",
#     "proxyPort": 4009,
#     "sheetID": "1xsKri9sMyFM1P-MD_zaniYs2mc3ZPeQEqIbONz4k2Qk"
# }
# result = app.update_file('TelegramCS/configs/configs.json',content)
# print(result)
# result = app.client.download_async(remote_path='TelegramCS/configs/configs.json',local_path=f'F:\py_project\TelegramIOS\modules\Temp\demo.json')

