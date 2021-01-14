#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from setuptools import setup
import __init__

setup(
    name='teimed2html',
    version=__init__.__version__,
    py_modules=['teimed2html'],
    scripts=[
        "copy2all.py",
        "htmlbuilder.py",
        "htmlformat.py",
        "htmloverflow.py",
        "info.py",
        "prjmgr.py",
        "readhtmlconf.py",
        "readjson.py",
        "splitteixml.py",
        "teixml2html.py",
        "uainput.py",
        "ualog.py",
        "writehtmlfile.py",
        "writehtml.py"
    ],
    author="Marta Materni",
    author_email="marta.materni@gmail.com",
    description="Tools per trasformare TEIML in HTML",
    long_description=open('README.rst').read(),
    include_package_data=True,
    url='http://github.com/gmaterni/mmtei',
    license="new BSD License",
    install_requires=['lxml'],
    classifiers=['Development Status :: 1 - Planing',
                 'Intended Audience :: Developers',
                 'License :: OSI Approved :: BSD License',
                 'Natural Language :: Italiano',
                 'Operating System :: OS Independent',
                 'Programming Language :: Python 3.6.',
                 'Topic :: Software Development :: Libraries',
                 'Topic :: Utilities'],
    entry_points={
        'console_scripts': [
            'teimed2htmlinfo = info:list_modules',
        ],
    },
)
