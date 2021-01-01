#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from pdb import set_trace


class Inp:
    """
    .   fine

        se debug_liv == 2:
    -   contimua senza print
    --  continua con print
            p='!' attiva input nel continua
            setta x==''
    ''  continua fino alla successiva
        continua fino al successivo tag eguale
        ?  visualiza html realizzato

        se debug_liv ==1:
        !  attiva input e disattiva tag settato

    """

    def __init__(self):
        self.debug = False
        self.pause = False
        self.x = ''
        self.last = ''
        self.ok_prn = True

    def set(self, debug_liv='0'):
        """livello debig
        0: disattivato
        1:  attivato solo per !
        2: attivato sempre input
        Args:
            debug_liv (int, optional): 0/1/2
        """       
        lv=int(debug_liv) 
        if lv == 1:
            self.pause = True
        elif lv == 2:
            self.debug = True

    def equals(self, s):
        return self.x == s

    @ property
    def prn(self):
        return self.ok_prn and self.debug

    def inp(self, p=''):
        stop = False
        if self.pause and p == '!':
            stop = True
            self.last = self.x
        if stop is False and self.debug is False:
            return
        # if self.debug is False:
        #   return
        enabled = False
        if self.x == '':
            enabled = True
        if self.x == '!':
            enabled = True
            self.x = ''
        elif self.x == p:
            enabled = True
        elif self.x == '?':
            enabled = True
            self.x = self.last
        elif self.x in ['-', '--']:
            enabled = False
        if p == '!':
            enabled = True
            self.x = ''
        if enabled or stop:
            if enabled :
                self.last = self.x
            s = input(p+'>')
            if s == '.':
                sys.exit()
            if s != '':
                self.x = s
            if s == '-':
                self.ok_prn = False
            else:
                self.ok_prn = True
