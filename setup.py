#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import find_packages
from setuptools import setup


setup(
    name='xivo_webi_plugins',
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
            'webihome = xivo_webi_plugins.home.plugin:Plugin',
            'fk = xivo_webi_plugins.funckeys.plugin:Plugin',
            'ctipassword = xivo_webi_plugins.ctipassword.plugin:Plugin',
            'generalsip = xivo_webi_plugins.generalsip.plugin:Plugin',
            'login_user = xivo_webi_plugins.login_user.plugin:Plugin',
            'bootstrap = xivo_webi_plugins.bootstrap.plugin:Plugin',
            'meetme = xivo_webi_plugins.meetme.plugin:Plugin',
        ],
    }
)

