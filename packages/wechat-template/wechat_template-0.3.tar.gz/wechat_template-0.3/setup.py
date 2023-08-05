# -*- coding: UTF-8 -*-
import os

import setuptools

setuptools.setup(
    name='wechat_template',
    version='0.3',
    keywords='',
    description='Django wx',
    long_description=open(
        os.path.join(
            os.path.dirname(__file__),
            'README.rst'
        )
    ).read(),
    author='yangcheng',
    author_email='yangcheng.fan@yuemia.com',

    url='',
    packages=setuptools.find_packages(),
    license='MIT')

