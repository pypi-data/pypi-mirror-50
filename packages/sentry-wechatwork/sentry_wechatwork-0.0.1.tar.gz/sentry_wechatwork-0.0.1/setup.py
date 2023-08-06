#!/usr/bin/env python
# coding: utf-8
from setuptools import setup

from sentry_wechatwork import __version__


with open('README.rst', 'r') as f:
    long_description = f.read()


setup(
    name='sentry_wechatwork',
    version=__version__,
    packages=['sentry_wechatwork'],
    url='https://github.com/kuainiu/sentry-wechatwork',
    author='Allen',
    author_email='hi@summic.com',
    description='Plugin for Sentry which allows sending notification via WechatWork messenger.',
    long_description=long_description,
    long_description_content_type='text/x-rst',
    license='MIT',
    entry_points={
        'sentry.plugins': [
            'sentry_wechatwork = sentry_wechatwork.plugin:WechatWorkNotificationsPlugin',
        ],
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Software Development :: Bug Tracking',
        'Topic :: Software Development :: Quality Assurance',
        'Topic :: System :: Monitoring',
    ],
    include_package_data=True,
)
