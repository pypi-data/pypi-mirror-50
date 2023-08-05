# -*- coding: UTF-8 -*-
import setuptools

with open("README.md", "r", encoding='utf8') as f:
    long_description = f.read()

setuptools.setup(
    name="zhihu-cli",
    version="1.1.0",
    author="zhangbo",
    author_email="deplives.zhang@gmail.com",
    description="zhihu",
    long_description=long_description,
    license="MIT",
    long_description_content_type="text/markdown",
    url="https://github.com/deplives/zhihu",
    packages=['zhihu'],
    install_requires=[
        'requests==2.21.0',
        'beautifulsoup4==4.7.1',
        'lxml==4.3.4',
    ],
    classifiers=(
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)
