# -*- coding:utf-8 -*-

import setuptools
from htjs_k8s import conf

setuptools.setup(
    name=conf.NAME,
    version=conf.VERSION,
    keywords=('htjs', 'htjs.net', 'k8s'),
    author="Mu Xiaofei",
    author_email="htjs.net@gmail.com",
    description="",
    long_description="",
    long_description_content_type="text/x-rst",
    url="",
    packages=setuptools.find_packages(),
    package_data={'': ["templates/*.yaml"]},
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=["six", "jinja2", "PyYAML", "colorama"],
    entry_points={
        "console_scripts": [
            "{}={}.cli:main".format(conf.NAME, conf.PACKAGE)
        ]
    },
)
