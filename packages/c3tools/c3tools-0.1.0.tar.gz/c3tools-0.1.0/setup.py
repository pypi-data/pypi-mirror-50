# -*- coding: utf-8 -*-
import os
from io import open
from setuptools import setup
from setuptools import find_packages

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, 'README.md'), "r", encoding="utf-8") as fobj:
    long_description = fobj.read()

requires = [
    "udp-test",
    "tcping",
    "ps2",
    "uname2",
    "ipa-utils",
    "sftpd",
    "python-sendmail",
    "filesplitor",
    "tail",
    "copytruncate",
    "pwgen",
    "zencore-json2csv",
    "python-json2yaml",
    "hashtools",
    "qrimg",
    "rot-codec",
    "transencoding",
    "xlsx-split",
    "xlsx-xargs",
    "pdf-tools",
    "makegif",
    "gif-frames",

]

setup(
    name="c3tools",
    version="0.1.0",
    description="Collections of simple commands.",
    long_description=long_description,
    long_description_content_type='text/markdown',
    author="zencore",
    author_email="dobetter@zencore.cn",
    license="MIT",
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
    ],
    keywords=['c3tools', 'cmdtools'],
    install_requires=requires,
    packages=find_packages("."),
)