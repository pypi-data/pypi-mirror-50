# _*_coding:utf-8_*_
"""
File: setup.py
Time: 2019/8/12 19:16
Author: ClassmateLin
Email: 406728295@qq.com
Desc: 
"""
from setuptools import setup, find_packages

VERSION = '1.0.0'

packages_info = {
    'name': 'Python-PayJs',
    'version': VERSION,
    'keywords': ['pip', 'PayJs', 'WeChat Pay'],
    'long_description': 'Python SDK for PayJS.',
    'license': 'MIT Licence',
    'url': "https://github.com/DrepMan/PyPayJs.git",
    'author': 'ClassmateLin',
    'author_email': '406728295@qq.com',
    'packages': find_packages(),
    'include_package_data': True,
    'platforms': 'any',
    'classifiers': [
        'Programming Language :: Python :: 3',
    ],
    'zip_safe': False,
    'install_requires': ['requests']
}

setup(**packages_info)