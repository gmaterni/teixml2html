#!/usr/bin/env python3
# coding: utf-8

from pdb import set_trace
import os
import stat

__date__ = "19-02-2021"
__version__ = "0.4.0"
__author__ = "Marta Materni"

"""
    Log("w")         modalità wrie
    Log("a")          modlaità append

    self.out_liv > 0   print attivato globalmente
    self.out_liv  <1    disattivato
    
    prn()/prn()          attivato localmente anche  
                         se distattivato globalmente
    prn(0)               disattivato localmente
                         ma resta valido il settaggio globale
"""


class Log(object):

    def __init__(self, aappend_write='w'):
        self.path_log = ""
        self.dirname=""
        self.aw = aappend_write
        self.out_liv = 0
        self.used = False
        self.msg = ''

    def set_liv(self, liv):
        self.out_liv = liv
        return self

    def open(self, path_log, liv):
        self.path_log = path_log
        self.dirname=os.path.dirname(path_log).strip()
        self.out_liv = int(liv)

    def open_file(self):
        if not os.path.exists(self.path_log):
           if not os.path.isdir(self.dirname):
                os.mkdir(self.dirname)
                os.chmod(self.dirname, stat.S_IRWXG + stat.S_IRWXU + stat.S_IRWXO)
        f=open(self.path_log,self.aw) 
        #f.write("")
        f.close()
        os.chmod(self.path_log, stat.S_IRWXG + stat.S_IRWXU + stat.S_IRWXO)
        
    def prn(self, liv=1):
        if self.out_liv ==0 and liv > 0:
            print(self.msg)
        return self

    def log(self, *args):
        if self.out_liv < 0:
            return self
        if not self.used:
            self.open_file()
            self.used=True
        ls = ["None" if x is None else str(x) for x in args]
        s = f"{os.linesep}".join(ls)
        f=open(self.path_log,"a")
        f.write(s)
        f.write(os.linesep)
        f.close()
        self.msg = s
        if self.out_liv > 0:
            print(s)
        return self
