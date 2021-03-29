#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import setup
from setuptools import find_packages
import teix2hlib.__init__

setup(
    name='teixml2html',
    version=teix2hlib.__init__.__version__,
    py_modules=['teixml2htmlinfo','ualog'],
    packages=find_packages(),
    scripts=[
        "prjmgr.py",
        "teiprjhtmlmake.py",
        "copyxml.py",
        "splitteixml.py",
        "teixml2html.py",
        "writehtmlfile.py",
        "writehtml.py"
    ],
    author="Marta Materni",
    author_email="marta.materni@gmail.com",
    description="Tools per trasformare XML TEI in HTML",
    long_description=open('README.rst').read(),
    include_package_data=True,
    url='https://github.com/digiflor/',
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
            'teixml2htmlinfo = info:list_modules',
        ],
    },
)
