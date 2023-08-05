import base64
import sys
import datetime
import hashlib
import hmac
import json
import requests
from binascii import b2a_hex, a2b_hex

from Crypto.Cipher import AES



class AesUtil:
    def __init__(self, key):
        len_key = len(key)
        assert len_key in [16, 24, 32], 'the length of SECRET_KEY must be 16 24 or 32'
        self.key = key
        self.iv = key
        self.mode = AES.MODE_CBC
        self.pad = lambda s: s + (len_key - len(s.encode('utf8')) % len_key) * chr(len_key - len(s.encode('utf8')) % len_key)
        self.unpad = lambda s: s[0:-ord(s[-1])]

    # 加密函数
    def encrypt(self, text):
        cryptor = AES.new(self.key, self.mode, self.iv)
        self.ciphertext = cryptor.encrypt(self.pad(text))
        # AES加密时候得到的字符串不一定是ascii字符集的，输出到终端或者保存时候可能存在问题，使用base64编码
        return b2a_hex(self.ciphertext).decode()

    # 解密函数
    def decrypt(self, text):
        # decode = base64.b64decode(text)
        cryptor = AES.new(self.key, self.mode, self.iv)
        plain_text = cryptor.decrypt(a2b_hex(text))
        return self.unpad(plain_text.decode())


def general_hmac(text, key):
    myhmac = hmac.new(key=key.encode(), digestmod=hashlib.sha256)
    myhmac.update(text.encode())
    return base64.b64encode(myhmac.digest()).decode()


def ti_request(username, secret_key, method, url, data=None):
    aes_utils = AesUtil(secret_key)
    GMT_FORMAT = '%a, %d %b %Y %H:%M:%S GMT'
    req_time = datetime.datetime.utcnow().strftime(GMT_FORMAT)
    signing_string = 'x-date: %s\nusername: %s' % (req_time, username)
    signature = general_hmac(signing_string, secret_key)
    headers = {
        'X-DATE': req_time,
        'username': username,
        'signature': signature,
    }
    print('headers', headers)
    if data:
        json_body = {'reqdata': aes_utils.encrypt(json.dumps(data))}
        print('body', json_body)
    else:
        json_body = None
        
    r = requests.request(method, url, json=json_body, headers=headers)

    try:
        res = r.json()
        if 'data' in res:
            data = res['data']
            data = aes_utils.decrypt(data)
            try:
                data = json.loads(data)
            except Exception as e:
                pass
            res['data'] = data
    except Exception as e:
        print(e)
        res = r.text

    return res


def tireq(args=None):
    # pip intall tisdk
    # tireq to_9012345678_grs 3292a4f76c0d46bf post http://taiqiyun.wowfintech.cn/grs/v1/open_match name:美团,foo:bar

    len_args = len(args)
    if len_args > 3:
        username = args[0]
        secret_key = args[1]
        method = args[2]
        url = args[3]
        data = args[4] if len_args > 4 else None
    else:
        # demo request
        username = 'to_9012345678_grs'
        secret_key = '3292a4f76c0d46bf'
        method = 'post'
        url = 'http://taiqiyun.wowfintech.cn/grs/v1/open_match'
        data = 'name:美团'

    if data:
        items = data.split(',')
        data = {item.split(':')[0]: item.split(':')[1] for item in items}

    res = ti_request(username, secret_key, method, url, data)
    print(res)


if __name__ == '__main__':
    # pip install requests pycrypto
    # python ti.py to_9012345678_grs 3292a4f76c0d46bf post http://taiqiyun.wowfintech.cn/grs/v1/open_match name:美团,foo:bar

    tireq(sys.argv[1:])

   
