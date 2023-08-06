# coding=utf-8

from setuptools import setup, find_packages

setup(
    name='f_luhn',
    version="0.0.1",
    description=(
        '一种连作者自己都看不明白的luhn校验码计算方案'

    ),
    author='fangzhao',  # 作者
    author_email='elpmis.fang@qq.com',
    license='BSD License',
    packages=find_packages(),
    platforms=["all"],
    url='https://github.com/tjgo/f_luhn'
)
