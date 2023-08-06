# -*- coding: utf-8 -*-
import setuptools

setuptools.setup(
    name="cron-lock",
    version="0.1.1",
    author="fallthrough",
    author_email="rainbroadcast@qq.com",
    description="A count lock recovered by periodicity",
    url="https://github.com/igzhang/cron_lock",
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 2.7',
    ],
    install_requires=[
        "six"
    ]
)
