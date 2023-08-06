# 引入构建包信息的模块
from distutils.core import setup

# 定义发布的包文件的信息
setup(
name = "flask-adh",  # 发布的包文件名称
version = "0.1",   # 发布的包的版本序号
description = "flask admin antd",  # 发布包的描述信息
author = "sleepingJ",   # 发布包的作者信息
author_email = "sleepingj@sina.com",  # 作者联系邮箱信息
py_modules = ['admin'],  # 发布的包中的模块文件列表
url = "https://github.com/sleepingj/flask-adh"
)
