# -*- coding: utf-8 -*-  

#from distutils.core import setup
import setuptools

with open("README.md", "r",encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name='autoleastsq',
    version='1.0.1',
    description='自动化拟合多项式，并自动判断最佳次幂',
    author='sheerfish',
    author_email='first@sheerfish.top',

    long_description=long_description,
    long_description_content_type="text/markdown",

    setup_requires=['scipy','xlrd','numpy'],

    packages = ['autoleastsq'],
    package_data = {'autoleastsq' : ["autoleastsq/*"] },

    classifiers=[
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
    ],
    )

