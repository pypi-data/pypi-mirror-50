# -*- coding:utf-8 -*-
from setuptools import find_packages, setup

setup(
    name='ucenter_sdk',
    version='1.0.13',
    packages=find_packages('src'),
    long_description=open('README.rst').read(),
    package_dir={'': 'src'},
    include_package_data=True,
    install_requires=['requests>=2.11.1'],
    author='shiwei.ma',
    author_email='shiwei.ma@yiducloud.cn',
    description='''YIDU UCenter SDK.''',
    keywords='user, ucenter',

)
