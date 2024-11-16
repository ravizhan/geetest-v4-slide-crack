# geetest-v4-slide-crack

极验四代滑块验证码破解

**本项目仅供学习交流使用，请勿用于商业用途，否则后果自负。**

**本项目仅供学习交流使用，请勿用于商业用途，否则后果自负。**

**本项目仅供学习交流使用，请勿用于商业用途，否则后果自负。**

# 使用方法

安装相关依赖

```commandline
pip install -r requirements.txt
```

运行

```commandline
python main.py
```

成功率在90%以上

# DEMO

``` python
from crack import Crack
crack = Crack("captcha_id", "https://static.geetest.com/v4/static/v1.8.5-5cf237/js/gcaptcha4.js") # 第二个参数须填入最新的JS地址
crack.load() # 加载验证码
res = crack.verify() # 校验验证码
print(res)
```

## 一些有趣的细节

### 关于缺口坐标

讲道理，这应该不难才对。用训练个YOLO模型检测一下就有了。检测结果画出来也没错，但就是死活对不上gcaptcha4.js中的结果。JS中是用初末位置的MouseEvent.clientX相减得到坐标，去查了相关定义，始终不知道那诡异的数是怎么来的。于是一气之下，打开excel，把JS中的坐标和检测出来的坐标丢进去，拟合线性函数。详见`crack.py` 84行。

### 关于验证码图片

两个月前爬验证码图片，做训练集来练YOLO。当时怎么爬都只有300张，我想可能每月或者每周都会更新一批吧。结果前几天再去爬，还是那些图，整得我怀疑人生了。于是大胆猜测，极验的图片库大概就那么些图片。遂导出之前的标注数据，也就是`data.json`，过验证码时直接读取坐标，实现光速提交。

# 协议

本项目遵循 AGPL-3.0 协议开源，请遵守相关协议。

# 鸣谢

[ultralytics](https://github.com/ultralytics/ultralytics/) 提供目标检测模型

[Geetest-AST-](https://github.com/daisixuan/Geetest-AST-) 提供一键反混淆JS

ChatGPT 提供逆向支持
