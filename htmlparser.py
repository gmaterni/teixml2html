#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pdb import set_trace
import os
import re
import sys
from lxml import etree
import pprint
import sys
import copy
import argparse
from readhtmlconf import read_html_conf
from readjson import read_json
from htmlbuilder import HtmlBuilder
from ualog import Log
from uainput import Inp

__date__ = "15-12-2020"
__version__ = "0.0.3"
__author__ = "Marta Materni"


def pp(data):
    if data is None:
        return ""
    s = pprint.pformat(data, indent=2, width=120)
    return s+os.linesep


loginfo = Log()
logerr = Log()
inp = Inp()


class HtmlParse(object):

    def __init__(self):
        loginfo.open("log/htmlparse.log", 0)
        logerr.open("log/htmlparse.err.log", 1)
        self.html_path = None
        
    def node_liv(self, node):
        d = 0
        while node is not None:
            d += 1
            node = node.getparent()
        return d - 1


    def node_items(self, nd):
        kvs = nd.items()
        js = {}
        for kv in kvs:
            v = kv[1]
            js[k] = v
        return js

    def node_tag(self, nd):
        tag = nd.tag
        tag = tag if type(nd.tag) is str else "XXX"
        p = tag.rfind('}')
        if p > 1:
            logerr.log("ERROR in  xml")
            logerr.log(nd.tag)
            sys.exyt()
        return tag.strip()

    def node_id(self, nd):
        s = ''
        kvs = nd.items()
        for kv in kvs:
            if kv[0].rfind('id') > -1:
                s = kv[1]
                break
        return s


    def node_text(self, nd):
        text = nd.text
        text = '' if text is None else text.strip()
        text = text.strip().replace(os.linesep, ',,')
        return text

    def node_tail(self, nd):
        tail = '' if nd.tail is None else nd.tail
        tail = tail.strip().replace(os.linesep, '')
        return tail

    def node_val(self, nd):
        ls = []
        for x in nd.itertext():
            s = x.strip().replace(os.linesep, '')
            ls.append(s)
        texts = ' '.join(ls)
        s = re.sub(r"\s{2,}", ' ', texts)
        return s

    def node_is_parent(self, nd):
        cs = nd.getchildren()
        l = len(cs)
        return l > 0

    def get_node_data(self, nd):
        items = self.node_items(nd)
        return {
            'id': id,
            'liv': self.node_liv(nd),
            'tag': self.node_tag(nd).lower(),
            'tail': self.node_tail(nd),
            'text': self.node_text(nd),
            'items': items,
            # 'val':self.node_val(nd),
            'is_parent': self.node_is_parent(nd)
        }


    def parse(self, html_path, deb=False):
        inp.enable(deb)        
        self.html_path = html_path
        try:
            root = etree.parse(self.html_path)
        except Exception as e:
            logerr.log(e)
            sys.exit()
        for nd in root.iter():
            nd_data=self.get_node_data(nd)
            tag=nd_data.get('tag',"")
            if inp.prn:
                loginfo.log(pp(nd_data)).prn()
            inp.inp(tag)
            if inp.equals('?'):
                print(pp(nd_data))
                inp.inp()


def do_mauin(html,deb):
    HtmlParse().parse(html,deb)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    if len(sys.argv) == 1:
        print("release: %s  %s" % (__version__, __date__))
        parser.print_help()
        sys.exit()
    parser.add_argument('-d',
                        dest="deb",
                        required=False,
                        action="store_true",
                        default=False,
                        help="[-d ](abilita debug)")
    parser.add_argument('-i',
                        dest="html",
                        required=True,
                        metavar="",
                        help="-i <file_in.html>")
    args = parser.parse_args()
    do_mauin(args.html, args.deb)
