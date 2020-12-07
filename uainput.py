#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys

   
"""
.   fine
-   contimua senza print
--  continua con print
        p='!' attiva input nel continua   
        setta x==''
''  continua fino alla successiva
    continua fino al successivo tag eguale
    ?  visualiza html realizzato
    !   attiva input e disattiva tag settato

"""


class Inp(object):

    def __init__(self):
        self.debug=False
        self.x = ''
        self.last=''
        self.ok_prn = True

    def enable(self,debug=False):
        self.debug=debug

    def equals(self,s):        
        return self.x==s    

    @property
    def prn(self):
        return self.ok_prn and self.debug    

    def inp(self,p=''):
        if self.debug is False:
            return
        enabled = False
        if self.x == '':
            enabled = True
        if self.x == '!':
            enabled = True
            self.x=''
        elif self.x == p:
            enabled = True
        elif self.x == '?':
            enabled = True
            self.x = self.last
        elif self.x in ['-','--']:
            enabled = False
        if p=='!':
            enabled=True
            self.x=''
        if enabled:
            self.last=self.x
            s = input(p+'>')
            if s== '.':
                sys.exit()
            if s!='':
                self.x=s
            if s== '-':
                self.ok_prn = False
            else:
                self.ok_prn = True
