#!/usr/bin/env python3
# coding: utf-8

import os

"""
    Log("w")         modalità wrie
    Log("a")          modlaità append

    self.out_liv > 0   print attivato globalmente
    self.out_liv  <1        disattivato
    
    prn()/prn()          attivato localmente anche  
                         se distattivato globalmente
    prn(0)               disattivato localmente
                         ma resta valido il settaggio globale
"""


class Log:

    def __init__(self, aappend_write='w'):
        self.used = False
        self.path_log = None
        self.aw = aappend_write
        self.out_liv = 0
        self.f = None
        self.msg = ''

    def set_liv(self, liv):
        self.out_liv = liv
        return self

    def open_log(self, path_log, liv=1):
        # ymd = str(datetime.datetime.today().strftime('%Y%m%d%H%M%S'))
        # ymd = str(datetime.datetime.today().strftime('%Y%m%d_%H_%M'))
        # self.path_log = path_log.replace('.log', f'_{ymd}.log')
        self.path_log = path_log
        self.out_liv = int(liv)
        self.f = None

    def open_fie(self):
        if self.used:
            return
        self.used = True
        self.f = open(self.path_log, self.aw)
        os.chmod(self.path_log, 0o666)
        
    def prn(self, out=1):
        if self.out_liv < 1 and out > 0:
            print(self.msg)
        return self

    def log(self, *args):
        if self.out_liv < 0:
            return self
        first = not self.used
        self.open_fie()
        ls = ["None" if x is None else str(x) for x in args]
        s = f"{os.linesep}".join(ls)
        if first:
            s = os.linesep+s
        self.f.write(s)
        self.f.write(os.linesep)
        self.f.flush()
        self.msg = s
        if self.out_liv > 0:
            print(s)
        return self
