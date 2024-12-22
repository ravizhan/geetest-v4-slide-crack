from crack import Crack
import time
crack = Crack("d7e4dfd8691a3cf54ab4df96787c4fef", "https://static.geetest.com/v4/static/v1.8.7-0a36ba/js/gcaptcha4.js")
crack.load()
# time.sleep(1) 似乎等不等都行
res = crack.verify()
print(res)
