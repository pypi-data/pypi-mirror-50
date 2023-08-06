# -*- coding:utf-8 -*-

import setuptools

setuptools.setup(
    name="htjs-k8s",
    version='0.0.2',
    keywords=("htjs", "htjs.net"),
    author="Mu Xiaofei",
    author_email="htjs.net@gmail.com",
    description="HtjsApiClient",
    long_description="",
    long_description_content_type="text/x-rst",
    url="",
    packages=setuptools.find_packages(),
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
            "htjs-k8s=htjs_k8s.cli:main"
        ]
    },
)
