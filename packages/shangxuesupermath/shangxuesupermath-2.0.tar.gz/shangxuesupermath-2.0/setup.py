from distutils.core import setup

setup(
    name='shangxuesupermath',     # 对外我们模块的名字
    version='2.0',           #版本号
    description='这是我第一个对外发布的模块，里面只有数学方法测试哦',   # 模块描述
    author='周贵川',   # 作者
    author_email='675097631@qq.com ',  #  作者邮箱
    py_modules=['shangxuesupermath.demo3','shangxuesupermath.demo4']  # 要发布的模块
)
