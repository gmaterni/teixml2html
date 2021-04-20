#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import stat
import os

def make_dir_of_file(path):
    dirname=os.path.dirname(path)
    if dirname.strip() =='':
        return
    make_dir(dirname)

def make_dir(dirname):
    try:
        if not os.path.isdir(dirname):
            os.mkdir(dirname)
            os.chmod(dirname, stat.S_IRWXG + stat.S_IRWXU + stat.S_IRWXO)
            return True
        else:
            return False
    except Exception as e:
        s=str(e)
        msg=f"ERROR make_dir{os.linesep}{s}"
        raise Exception(msg)

def chmod(path):
    os.chmod(path, stat.S_IRWXG + stat.S_IRWXU + stat.S_IRWXO)
