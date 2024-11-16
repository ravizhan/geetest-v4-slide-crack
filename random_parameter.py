import re
import urllib.parse

def get_random_parameter(js):
    def decode_and_split(encoded_str, key):
        decoded_str = urllib.parse.unquote_plus(encoded_str, errors="")
        result = ""
        a = 0
        for i in range(len(decoded_str)):
            if a == 6:
                a = 0
            xor_char = chr(ord(decoded_str[i]) ^ ord(key[a]))
            result += xor_char
            a += 1
        return result.split('^')

    param = re.findall(r'''".{24}": .*\(..\)''', js)[0].encode('utf-8').decode('unicode_escape')
    param1 = param.split(":")[0].strip('"')
    param2 = param[-3:-1]
    encoded_str = re.findall(r'''decodeURI.*\);''', js)[0][10:-2]
    key = re.findall(r'''\('.{6}'\)''', js)[0][2:-2]
    string_list = decode_and_split(eval(encoded_str), key)
    param2 = string_list[int(param2)]
    return param1, param2
