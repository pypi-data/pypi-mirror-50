import codecs
import os
import sys

try:
    from setuptools import setup
except:
    from distutils.core import setup

 
NAME = "jibu"
PACKAGES = ["package"]
DESCRIPTION = "this is a test"
AUTHOR = "bkb0813"
VERSION = "1.0"
LICENSE = "MIT"

URL = "https://pypi.org/manage/projects/"
AUTHOR_EMAIL = "2496821934@qq.com",

setup(
    name = NAME,
    version = VERSION,
    description = DESCRIPTION,
#     classifiers = [
#         'License :: OSI Approved :: MIT License',
#         'Programming Language :: Python',
#         'Intended Audience :: Developers',
#         'Operating System :: OS Independent',
#     ],
#     author = AUTHOR,
#     author_email = AUTHOR_EMAIL,
#     url = URL,
    license = LICENSE,
    packages = PACKAGES
)