#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pdb import set_trace
from ualog import Log
from uainput import Inp
import pprint

def pp(data):
    if data is None:
        return ""
    s = pprint.pformat(data, indent=2, width=120)
    return s+os.linesep

loginfo = Log()
logerr = Log()
inp = Inp()


class HtmlOvweflow(object):

    def __init__(self,xml_lst,html_lst,deb=False):
        self.deb=deb
        loginfo.open("log/htmloverflow.log", 0)
        logerr.open("log/htmloverflow.err.log", 1)
        self.xml_lst=xml_lst
        self.html_lst=html_lst
        self.span_lst=None

    # <span from="Gl23w1" to="Gl98w6" type="directspeech"/>

    def set_span_list(self):
        for x in self.xml_lst:
            x_tag=x.get('tag','')
            if x_tag=='span':
                x_items=x.get('items',{})
                x_from =x_items.get('from','')
                x_to =x_items.get('to','')
                x_type =x_items.get('type','')
                print(f'{x_from }  {x_to}  {x_type}')

    def set_overflow(self):
        self.set_span_list()

