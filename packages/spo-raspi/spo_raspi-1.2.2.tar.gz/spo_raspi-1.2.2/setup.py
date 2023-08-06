#!/usr/bin/env python3
#-*- coding:utf-8 -*-

#############################################
# File Name: setup.py
# Author: AW
# Mail: weidacn@qq.com
# Created Time:  2019-7-29
# Update Time:  2019-8-10
#############################################


from setuptools import setup, find_packages            #这个包没有的可以pip一下


setup(
    name = "spo_raspi",      #这里是pip项目发布的名称
    version = "1.2.2",  #版本号，数值大的会优先被pip
    keywords = ("raspi"),
    description = "SPO",
    long_description = "A tool to control servo,RFID,Baidu speech API,and emotibot API in raspberry Pi\n"
                       "Update:fix a bug in RFID reading",
    license="MIT",
    url = "https://github.com/weidacn/SPO_raspi",
    author='AW',
    author_email='weidacn@qq.com',
    
    packages = find_packages(),
    include_package_data = True,
    platforms = "any",
    install_requires = ["pi-rc522","baidu-aip","adafruit-pca9685"]          #这个项目需要的第三方库
)
