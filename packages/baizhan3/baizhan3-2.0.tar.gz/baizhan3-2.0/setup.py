from distutils.core import setup

setup(
    name='baizhan3',     # 对外我们模块的名字
    version='2.0',           #版本号
    description='这是我第一个对外发布的模块，里面只有数学方法测试哦',   # 模块描述
    author='周贵川',   # 作者
    author_email='zhouguichuan520@163.com',  #  作者邮箱
    py_modules=['baizhan3.001','baizhan3.002']  # 要发布的模块
    )