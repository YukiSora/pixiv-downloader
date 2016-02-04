# pixiv-downloader
功能简陋的 Pixiv 下载器，使用 Pixiv public api 实现下载每日排行榜的图片。

##使用方法
需要在同级目录下创建文件 `history.json`，内容为空 json `{}`，目的是储存下载过的图片 id 避免重复下载。<br>
启动方法：<br>
` python pixiv.py`

##使用环境
1. Python 3: https://www.python.org/downloads/release/python-351/
2. Request: http://www.python-requests.org/en/master/user/install/#install
