# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(

    name='lemay_ai_sidecar',

    version="0.0.1",

    packages=['lemay_ai_sidecar'],

    package_data={'': ['*.csv',]},

    include_package_data=True,

    install_requires=["pandas>=0.24.*","Keras>=2.2.4","scikit-learn>=0.21.3","scipy>=0.17.0","tensorflow>=1.11.*,<1.14.*","numpy>=1.16.*","gensim>=3.8.0","wget>=3.2"],

)
