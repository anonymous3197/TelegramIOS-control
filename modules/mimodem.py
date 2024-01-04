#%%
import requests


import time, random
import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

class Encrypt:
    def __init__(self):
        self.key = 'a2ffa5c9be07488bbb04a3a47d3c5f6a'
        self.iv = '64175472480004614961023454661220'
        self.nonce = None

    def init(self):
        nonce = self.nonce_creat()
        self.nonce = nonce
        return self.nonce

    def nonce_creat(self):
        type = 0
        deviceId = '3c:ec:ef:7a:64:b3'
        t = int(time.time())
        rand = random.randint(0, 9999)
        return '_'.join(str(x) for x in [type, deviceId, t, rand])

    def old_pwd(self, pwd):
        nonce_pwd = self.nonce + hashlib.sha1((pwd + self.key).encode()).hexdigest()
        return hashlib.sha1(nonce_pwd.encode()).hexdigest()

    def new_pwd(self, pwd, newpwd):
        key = hashlib.sha1((pwd + self.key).encode()).hexdigest()
        key = bytes.fromhex(key)[:16]
        password = hashlib.sha1((newpwd + self.key).encode()).hexdigest()
        iv = bytes.fromhex(self.iv)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        aes = cipher.encrypt(pad(password.encode(), AES.block_size)).hex()
        return aes

class MiModem:
    def __init__(self, host = '192.168.3.1', username = 'admin', password = 'Tu@n0910#z') -> None:
        self._host = host
        self._password = password
        self._username = username
        self.token = None
        self.ss = requests.Session()
        self.login()

    def list_devices(self, filter_string = None):
        if self.token is None:
            return
        res = self.ss.get(
            f'http://{self._host}/cgi-bin/luci/;stok={self.token}/api/misystem/devicelist',
            verify=False,
        )
        devices = res.json()['list']
        if filter_string:
            output = [{'name' : d['name'], 'ip': d['ip'][0]['ip']} for d in devices]
            output = list(filter(lambda d: filter_string.lower() in d["name"].lower(), output))
        else:
            output = [{'name' : d['name'], 'ip': d['ip'][0]['ip']} for d in devices]
        return output

    def login(self):
        try:
            encrypt = Encrypt()
            nonce = encrypt.init()
            password = encrypt.old_pwd(self._password)

            headers = {
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            }
            data = {
                'username': self._username,
                'password': password,
                'logtype': '2',
                'nonce': nonce,
            }
            res = self.ss.post(
                'http://192.168.3.1/cgi-bin/luci/api/xqsystem/login',
                headers=headers,
                data=data,
                verify=False,
            )
            self.token = res.json()['token']
            return res.json()['token']
        except Exception as e:
            print('ERROR:login:', e)
            return False

# mi = MiModem()
# devices = mi.list_devices('iPhone')
# print(devices)
