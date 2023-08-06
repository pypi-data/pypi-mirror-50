# coding:utf-8

from setuptools import setup
from setuptools import find_packages
pack = find_packages(exclude=[''])
print(pack)
setup(
    name='UUO',
    version='0.0.13',
    # packages=['catch'],
    py_modules=['catch'],
    url='http://mrongm.online',
    author='idskof@sina.cn'
)