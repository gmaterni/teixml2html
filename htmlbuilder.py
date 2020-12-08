#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from pdb import set_trace

BLKS = "                                                         "
NL = os.linesep


class HtmlBuilder(object):

    def __init__(self):
        self.indent = 2
        self.livx = -1
        self.node_lst = []
        self.tag_stack = ['' for i in range(20)]
        self.tail_stack = ['' for i in range(20)]

    def sp(self, liv):
        return BLKS[0: liv * self.indent]

   # <!DOCTYPE html>
    def init(self, decl=""):
        if decl != "":
            self.node_lst.append(decl)
        return self

    def opn(self, liv, tag, attrs, text, tail):
        self.clsopn(liv)
        self.livx = liv
        self.tag_stack[liv] = tag
        self.tail_stack[liv] = tail
        b = '' if attrs == '' else ' '
        sp = self.sp(liv)
        if tag.find('>')>-1:
            tag=tag.split('>')[0]
        t = f'{sp}<{tag}{b}{attrs}>{text}'
        self.node_lst.append(t)
        return self

    def ovc(self, liv, tag, attrs, text, tail):
        if self.clsopn(liv):
            self.livx = liv - 1
        b = '' if attrs == '' else ' '
        sp = self.sp(liv)
        if tag.find('>')>-1:
            tag=tag.split('>')[0]
        if text != '':
            t = f'{sp}<{tag}{b}{attrs}>{text}</{tag}>{tail}'
        else:
            t = f'{sp}<{tag}{b}{attrs}/>{tail}'
        self.node_lst.append(t)
        return self

    def clsopn(self, liv):
        if liv > self.livx:
            return False
        for i in range(self.livx, liv - 1, -1):
            tag = self.tag_stack[i]
            tail = self.tail_stack[i]
            sp = self.sp(i)
            if tag.find('>')>-1:
                ts=tag.split('>')
                tag=ts[0]                
                tag_child=f'</{ts[1]}>' 
            else:               
                tag_child=''
            t = f'{sp}{tag_child}</{tag}>{tail}'
            self.node_lst.append(t)
        return True


    # rimuove tutte le righe che contengono tag
    def del_tags(self, tag):
        ls = []
        for nd in self.node_lst:
            if nd.find(tag) < 0:
                ls.append(nd)
        self.node_lst = ls


    # chiusura con ultimo tag
    def end(self):
        self.clsopn(0)
        return self

    # ultimo tag costruito
    def tag_last(self):
        return self.node_lst[-1:][0]

    # html identato
    def html_format(self):
        s = os.linesep.join(self.node_lst)
        return s

    # html su una sola riga eliminati spazi tra i tag
    def html_onerow(self):
        ls=[x.strip() for x in self.node_lst]
        s = "".join(ls)
        return s


