import hashlib
import json
import time
import random
import httpx
import uuid
from detect import Detect
from random_parameter import get_random_parameter
from cryptography.hazmat.primitives import padding, serialization
from cryptography.hazmat.primitives.asymmetric.padding import PKCS1v15
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes


class Crack:
    def __init__(self, captcha_id, gcaptcha4_url):
        self.left_pos = None
        self.pow_detail = None
        self.payload = None
        self.lot_number = None
        self.process_token = None
        self.bg = None
        self.captcha_id = captcha_id
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
        }
        self.httpx_session = httpx.Client(http2=True, headers=self.headers, verify=False)
        self.aes_key = ''.join(f'{int((1 + random.random()) * 65536):04x}'[1:] for _ in range(4)).encode()
        public_key = '''-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDB45NNFhRGWzMFPn9I7k7IexS5
XviJR3E9Je7L/350x5d9AtwdlFH3ndXRwQwprLaptNb7fQoCebZxnhdyVl8Jr2J3
FZGSIa75GJnK4IwNaG10iyCjYDviMYymvCtZcGWSqSGdC/Bcn2UCOiHSMwgHJSrg
Bm1Zzu+l8nSOqAurgQIDAQAB
-----END PUBLIC KEY-----'''
        self.public_key = serialization.load_pem_public_key(public_key.encode())
        self.enc_key = self.public_key.encrypt(self.aes_key, PKCS1v15()).hex()
        self.detect = Detect().detect
        self.param1,self.param2 = get_random_parameter(self.httpx_session.get(gcaptcha4_url).text)

    def load(self):
        url = "https://gcaptcha4.geetest.com/load"
        params = {
            "callback": "geetest_" + str(round(time.time() * 1000)),
            "captcha_id": self.captcha_id,
            "challenge": str(uuid.uuid4()),
            "client_type": "web",
            "risk_type": "slide",
            "lang": "zh",
        }
        res = self.httpx_session.get(url, params=params).text
        data = json.loads(res[22:-1])["data"]
        # self.slice = data["slice"]
        self.bg = "https://static.geetest.com/" + data["slice"].replace("slice", "bg")
        self.process_token = data["process_token"]
        self.lot_number = data["lot_number"]
        self.payload = data["payload"]
        self.pow_detail = data["pow_detail"]
        return data

    def verify(self):
        url = "https://gcaptcha4.geetest.com/verify"
        params = {
            "callback": "geetest_" + str(round(time.time() * 1000)),
            "lot_number": self.lot_number,
            "captcha_id": self.captcha_id,
            "process_token": self.process_token,
            "client_type": "web",
            "risk_type": "slide",
            "payload_protocol": "1",
            "pt": "1",
            "payload": self.payload,
            "w": ""
        }
        pow_res = self.pow()
        img_file_name = self.bg.split("/bg/")[1][:-4]
        with open("data.json", "r") as f:
            database = json.load(f)
        content = self.httpx_session.get(self.bg).content
        img_hash = hashlib.md5(content).hexdigest()
        if img_hash in database.keys():
            print(img_file_name, "in database")
            left_pos = database[img_hash]
        else:
            print(img_file_name, "not in database")
            # 别问为什么表达式这么诡异，问就是excel拟合出来的
            left_pos = int(self.detect(content)[0]*0.9862-11.317)
        e = {
            "setLeft": left_pos,
            "passtime": 1028,
            "userresponse": left_pos / 1.0059466666666665 + 2,
            "device_id": "",
            "lot_number": self.lot_number,
            "pow_msg": pow_res["pow_msg"],
            "pow_sign": pow_res["pow_sign"],
            "geetest": "captcha",
            "lang": "zh",
            "ep": "123",
            "biht": "1426265548",
            "gee_guard": {
                "roe": {
                    "aup": "3",
                    "sep": "3",
                    "egp": "3",
                    "auh": "3",
                    "rew": "3",
                    "snh": "3",
                    "res": "3",
                    "cdc": "3"
                }
            },
            self.param1: self.param2,
            "em": {
                "ph": 0,
                "cp": 0,
                "ek": "11",
                "wd": 1,
                "nt": 0,
                "si": 0,
                "sc": 0
            }
        }
        w = self.aes_encrypt(json.dumps(e, separators=(',', ':'))) + self.enc_key
        params["w"] = w
        # print(params)
        res = self.httpx_session.get(url, params=params).text[22:-1]
        return json.loads(res)

    def aes_encrypt(self, content: str):
        cipher = Cipher(algorithms.AES(self.aes_key), modes.CBC(b"0000000000000000"))
        encryptor = cipher.encryptor()
        padder = padding.PKCS7(128).padder()
        padded_data = padder.update(content.encode())
        padded_data += padder.finalize()
        ct = encryptor.update(padded_data) + encryptor.finalize()
        s = []
        for byte in ct:
            s.append(byte)
        return self.arrayToHex(s)

    @staticmethod
    def arrayToHex(e) -> str:
        t = [0] * ((2 * len(e) + 7) // 8)
        s = 0

        for n in range(0, 2 * len(e), 2):
            t[n >> 3] |= int(e[s]) << (24 - (n % 8) * 4)
            s += 1

        i = []

        for r in range(len(e)):
            o = (t[r >> 2] >> (24 - (r % 4) * 8)) & 255
            i.append(format(o >> 4, 'x'))
            i.append(format(o & 15, 'x'))

        return ''.join(i)

    def pow(self):
        temp = [self.pow_detail["version"], str(self.pow_detail["bits"]), self.pow_detail["hashfunc"], self.pow_detail["datetime"], self.captcha_id,
                self.lot_number]
        c = "|".join(temp) + "||"
        h = ''.join(f'{int((1 + random.random()) * 65536):04x}'[1:] for _ in range(4))
        match self.pow_detail["hashfunc"]:
            case "md5":
                p = hashlib.md5((c + h).encode()).hexdigest()
            case "sha1":
                p = hashlib.sha1((c + h).encode()).hexdigest()
            case "sha256":
                p = hashlib.sha256((c + h).encode()).hexdigest()
        return {"pow_msg": c + h, "pow_sign": p}


