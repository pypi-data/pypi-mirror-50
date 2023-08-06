import codecs
import os
import sys
try:
    from setuptools import setup
except:
    from distutils.core import setup

"""
打包的用的setup必须引入，

"""

NAME = "aiLearning"

PACKAGES = ["aiLearning", ]

DESCRIPTION = "this is a package for packing python machine learning."  # 模块描述，可选改

url =  'https://github.com/apachecn/AiLearning'
KEYWORDS = "python package"  # 关键字，可选改

VERSION = "1.7.6"

LICENSE = "MIT"


setup(
    name = NAME,
    version = VERSION,
    description = DESCRIPTION,
    classifiers = [
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
    ],
    keywords = KEYWORDS,
    license = LICENSE,
    packages = PACKAGES,
    include_package_data = True,
    zip_safe = True,
    # install_requires =['paramiko']
)