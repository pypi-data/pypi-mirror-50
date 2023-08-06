#发布文件

from distutils.core import setup
setup(
    name='math1',    #对 外 我 们 模 块 的 名 字
    version='1.0',  #版本号
    description="发布的第一个模块" , #描 述
    author='regan', #作 者
    author_email='regan110@163.com',
    py_modules=['math1.math01','math1.math02']  #要 发 布 的 模 块
)
