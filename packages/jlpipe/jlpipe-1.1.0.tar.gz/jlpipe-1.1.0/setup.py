#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

try:
    README = open('README.md').read()
except Exception:
    README = ""
VERSION = "1.1.0"

requirments = ["click"]

setup(
    name='jlpipe',
    version=VERSION,
    description='jlpipe',
    url="https://github.com/yjmade/jlpipe",
    long_description=README,
    long_description_content_type="text/markdown",
    author='Jay Young',
    author_email='dev@yjmade.net',
    packages=find_packages(),
    install_requires=requirments,
    extras_require={
        # "extra": ["extra_requirments"],
    },
    entry_points={
        'console_scripts': [
            'dynamojson=jlpipe:convert_dynamojson_cmd',
            'jsonkey=jlpipe:json_keys_cmd',
            "jsonallkeys=jlpipe:json_keys_total_cmd",
            'jsonselect=jlpipe:json_select_cmd',
            'parallel_split=jlpipe:parallel_split',
            "json2csv=jlpipe:json2csv",
            "json2pgtext=jlpipe:json2pgtext",
            "json2sqlite=jlpipe:json_to_sqlite",
            "parquet2json=jlpipe:parquet2json",
            "jsondecompress=jlpipe:decompress_binary_fields",
            "linedecompress=jlpipe:decompress_full_line",
            "arrayunpack=jlpipe:array_unpack",
            "pgcopy=jlpipe:pgcopy",
        ]
    },
)
