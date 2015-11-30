#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import find_packages
from setuptools import setup


setup(
    name='xivo_webi',
    version='0.1',

    description='XiVO webi',

    author='Sylvain Boily',
    author_email='sboily@avencall.com',

    url='https://github.com/sboily/xivo-webi-plugins',

    packages=find_packages(),
    include_package_data = True,
    zip_safe = False,

    entry_points={
        'xivo_webi.plugins': [
            'webihome = xivo_webi.plugins.home:Plugin',
            'fk = xivo_webi.plugins.funckeys:Plugin',
            'ctipassword = xivo_webi.plugins.ctipassword:Plugin',
            'generalsip = xivo_webi.plugins.generalsip:Plugin',
            'login_user = xivo_webi.plugins.login_user:Plugin',
        ],
    }
)

