#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from pdb import set_trace


class Inp:
    """livello debig
    0: disattivato attivato per !!
    1: attivato solo per !
    2: attivato sempre input
    Args:
        debug_liv (int, optional): 0/1/2
    """

    def __init__(self):
        self.liv = 0
        self.last = '$'
        self.ok_prn = False

    def set_liv(self, liv='0'):
        if self.liv < 0:
            return
        self.liv = int(liv)
        self.ok_prn=(self.liv>0)

    def equals(self, s):
        return self.last == s

    @ property
    def prn(self):
        return self.ok_prn

    def inp(self, p=''):
        ok=False
        if self.liv==0:
            return
        elif self.liv==1:
            if p=='!':
                ok=True
                self.last=p
        elif self.liv==2:
            ok=True
        if not ok:
            return
        if self.last=='$':
            self.last=p
        if self.last==p:
            v = input(p+'>')
            if v == '.':
                sys.exit()
            elif v == '-':
                self.liv = -1
                self.ok_prn = False
            elif v == '--':
                self.liv = -1
                self.ok_prn = True
            elif v=='?':
                pass
            elif v!='':
                self.last=v




