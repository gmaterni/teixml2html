#!/usr/bin/env python3
# coding: utf-8
# import datetime
import os
from pdb import set_trace

"""
    self.out > 0 print attivato globalmente
    self.oout <1        disattivato
    prn(1)              attivato
"""
class Log(object):

    def __init__(self):
        self.used = False
        self.path_log =None
        self.out = 0
        self.f = None
        self.msg=''

    def set_out(self,out):
        self.out=out
        return self

    def open (self, path_log, out=1):
        # ymd = str(datetime.datetime.today().strftime('%Y%m%d%H%M%S'))
        # ymd = str(datetime.datetime.today().strftime('%Y%m%d_%H_%M'))
        # self.path_log = path_log.replace('.log', f'_{ymd}.log')
        self.path_log = path_log
        self.out = int(out)
        self.f = None

    def open_fie(self):
        if self.used:
            return
        self.used = True
        self.f = open(self.path_log, "w")
        os.chmod(self.path_log, 0o666)

    def prn(self,out=1):
        if self.out <1 and out > 0:
            print(self.msg)
        return self

    def log(self, *args):
        self.open_fie()
        ls=["None" if x is None else str(x) for x in args]
        s=", ".join(ls)
        self.f.write(s)
        self.f.write(os.linesep)
        self.f.flush()
        self.msg=s
        if self.out > 0:
            print(s)
        return self
