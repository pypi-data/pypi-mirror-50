from distutils.core import setup

setup(
name='fxw_test_fabu', # 对外我们模块的名字
version='1.0', # 版本号
description='这是第一个对外发布的模块，测试哦', #描述
author='fxw', # 作者
author_email='fxiaowei@outlook.com',
py_modules=['fabu.mypy01','fabu.mypy02'] # 要发布的模块
)