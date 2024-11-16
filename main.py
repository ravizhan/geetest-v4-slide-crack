from crack import Crack
import time
crack = Crack("54088bb07d2df3c46b79f80300b0abbe", "https://static.geetest.com/v4/static/v1.8.5-5cf237/js/gcaptcha4.js")
crack.load()
# time.sleep(1) 似乎等不等都行
res = crack.verify()
print(res)
