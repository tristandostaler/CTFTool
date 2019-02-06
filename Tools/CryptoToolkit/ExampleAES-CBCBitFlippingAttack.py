import codecs
import json 
from hashlib import md5 
from base64 import b64decode 
from base64 import b64encode 
from Crypto import Random 
from Crypto.Cipher import AES 


class AESCipher: 
    """ 
    Usage: 
        c = AESCipher('password').encrypt('message') 
        m = AESCipher('password').decrypt(c) 
    Tested under Python 3 and PyCrypto 2.6.1. 
    """ 
 
    def __init__(self, key): 
        self.key = md5(key).hexdigest() 
 
    def encrypt(self, raw): 
        raw = pad(raw) 
        iv = b'a'*16 
        cipher = AES.new(self.key.encode("utf8"), AES.MODE_CBC, iv) 
        return b64encode(iv + cipher.encrypt(raw.encode())) 
 
    def decrypt(self, enc): 
        enc = b64decode(enc) 
        iv = enc[:16] 
        cipher = AES.new(self.key.encode(), AES.MODE_CBC, iv) 
        return unpad(cipher.decrypt(enc[16:])).decode('utf8') 

BLOCK_SIZE = 16  # Bytes 
pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * \
                chr(BLOCK_SIZE - len(s) % BLOCK_SIZE) 
unpad = lambda s: s[:-ord(s[len(s) - 1:])] 


secret_key = b'seed removed'
flag_value = b'flag removed'

cookie = {} 
cookie['password'] = "test"
cookie['username'] = "test"
cookie['admin'] = 0


print(cookie) 
cookie_data = json.dumps(cookie, sort_keys=True) 
encrypted = AESCipher(secret_key).encrypt(cookie_data) 
print(encrypted)
hex_data = b64decode(encrypted).hex()
print(hex_data)

for i in range(0,160):
    for h in range(0, 256):
        try:
            h1 = "{:02x}".format(h)
            hex_data_modified = hex_data[:i] + h1 + hex_data[i+2:] 

            hex_data2 = codecs.decode(hex_data_modified, 'hex')
            encrypted2 = b64encode(hex_data2)
            decrypted = AESCipher(secret_key).decrypt(encrypted2)
            data = json.loads(decrypted)
            if data['admin'] == 1:
                print("index: " + str(i) + " " + decrypted)
            #print(data)
        except:
            pass

'''

IV Before: 61616161616161616161616161616161
IV After:  61616161616161616161146161616161 

Corresponding flipping:
61616161616161616161146161616161
{ " a d m i n " :   1 ,   " p a ...

From:
Before: {"admin": 0, "password": "test", "username": "test"}
After:  {"admin": 1, "password": "test", "username": "test"}

'''