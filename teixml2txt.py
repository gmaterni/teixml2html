#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import argparse
import os
from io import StringIO
import pprint
import re
import sys
import traceback
from lxml import etree
from teixml2lib.txtbuilder import TxtBuilder
from teixml2lib.readtxtconf import read_text_tag
from teixml2lib.readjson import read_json
from teixml2lib.uainput import Inp
from teixml2lib.ualog import Log
import teixml2lib.prndata as pd
from teixml2lib import file_utils as fu
from pdb import set_trace

__date__ = "20-04-2021"
__version__ = "0.2.1"
__author__ = "Marta Materni"


def pp(data,w=40):
    s = pprint.pformat(data, indent=2, width=40)
    return s

inp = Inp()

class Xml2Txt:

    def __init__(self):
        self.log=Log("w")
        self.log.open("log/teixml2txt.log", 0)
        self.logerr = Log("a")
        self.logerr.open("log/teixml2txt.ERR.log", 1)
        self.xml_path = ''
        self.txt_path = None
        self.txt_builder = None
        self.trace = False

    def node_liv(self, node):
        d = 0
        while node is not None:
            d += 1
            node = node.getparent()
        return d - 1

    def clean_key(self, k):
        s = k
        p0 = k.find("{http")
        if (p0 > -1):
            p1 = k.rfind('}')
            if p1 > -1:
                s = k[p1+1:]
        return s

    def node_items(self, nd):
        kvs = nd.items()
        js = {}
        for kv in kvs:
            k = self.clean_key(kv[0])
            v = kv[1]
            js[k] = v
        return js

    def node_tag(self, nd):
        try:
            tag = nd.tag
            tag = tag if type(nd.tag) is str else "XXX"
            pid = tag.find('}')
            if pid > 0:
                tag = tag[pid + 1:]
            return tag.strip()
        except Exception as e:
            self.logerr.log("ERROR in xml")
            self.logerr.log(str(e))
            return "XXX"

    def node_id(self, nd):
        s = ''
        kvs = nd.items()
        for kv in kvs:
            if kv[0].rfind('id') > -1:
                s = kv[1]
                break
        return s

    def node_id_num(self, id):
        if id == '':
            return ''
        m = re.search(r'\d', id)
        if m is None:
            return -1
        p = m.start()
        return id[p:]

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
        le = len(cs)
        return le > 0

    def get_node_data(self, nd):
        items = self.node_items(nd)
        id = self.node_id(nd)
        if id != '':
            id_num = self.node_id_num(id)
            items['id_num'] = id_num
        js={
            'id': id,
            'liv': self.node_liv(nd),
            'tag': self.node_tag(nd),
            'text': self.node_text(nd),
            'tail': self.node_tail(nd),
            'items': items,
            # 'keys': self.node_keys(nd)
            # 'val': self.node_val(nd),
            'val': "",
            'is_parent': self.node_is_parent(nd)
        }
        return js

    def build_txt_data(self, nd):
        """ crea un json contenente
        x_data (estratto da xml)
        t_data (empty per la furua elaborazione)
        Args:
            nd : nod xml
        Returns:
            json: json=x_data + c_data + t_data
        """        
        x_data = self.get_node_data(nd)
        txt_data = {
            'id': x_data.get('id',0),
            'is_parent':x_data.get('is_parent',False),
            'items': x_data.get('items',{}),
            'liv': x_data.get('liv',0),
            'tag': x_data.get('tag',''),
            'text': x_data.get('text',''),
            'tail': x_data.get('tail',''),
            'val': x_data.get('val',''),
            't_i':0,
            't_type':'',
            't_up':False,
            't_start':'',          
            't_end':'',
            't_sp':'',
            't_ln':False,
            't_flag':False
            }
        return txt_data
    
    def write_txt(self,
                  xml_path='',
                  txt_path='',
                  write_append = 'w',
                  debug_liv = '0'):
        try:
            inp.set_liv(debug_liv)
            self.xml_path=xml_path
            self.txt_path=txt_path
            if write_append not in ['w', 'a']:
                raise Exception(
                    f"ERROR in output write/append. {write_append}")
            try:
                parser = etree.XMLParser(ns_clean=True)
                xml_root=etree.parse(self.xml_path,parser)
            except Exception as e:
                self.logerr.log("ERROR teixml2txt.py write_txt() parse_xml")
                self.logerr.log(e)
                sys.exit(str(e))
            self.txt_builder=TxtBuilder()
            ########################
            for nd in xml_root.iter():
                txt_data=self.build_txt_data(nd)
                self.txt_builder.add(txt_data)
            ########################
            self.txt_builder.elab()           
            txt=self.txt_builder.txt
            fu.make_dir_of_file(self.txt_path)
            with open(self.txt_path, write_append) as f:
                f.write(txt)
            fu.chmod(self.txt_path)

        except Exception as e:
            self.logerr.log("ERROR teixml2txt.py write_html()")
            self.logerr.log(e)
            ou=StringIO()
            traceback.print_exc(file = ou)
            st=ou.getvalue()
            ou.close()
            self.logerr.log(st)
            sys.exit(1)
        return self.txt_path

def do_mauin(xml, txt, wa = 'w', deb = False):
    Xml2Txt().write_txt(xml, txt, wa, deb)

if __name__ == "__main__":
    parser=argparse.ArgumentParser()
    if len(sys.argv) == 1:
        print("release: %s  %s" % (__version__, __date__))
        parser.print_help()
        sys.exit(1)
    parser.add_argument('-d',
                        dest = "deb",
                        required = False,
                        metavar = "",
                        default = 0,
                        help = "[-d 0/1/2](setta livello di debug)")
    parser.add_argument('-wa',
                        dest = "wa",
                        required = False,
                        metavar = "",
                        default = "w",
                        help = "[-wa w/a (w)rite a)ppend) default w")
    parser.add_argument('-i',
                        dest = "xml",
                        required = True,
                        metavar = "",
                        help = "-i <file_in.xml>")
    parser.add_argument('-o',
                        dest = "txt",
                        required = True,
                        metavar = "",
                        help = "-o <file_out.txt>")
    args=parser.parse_args()
    do_mauin(args.xml, args.txt, args.wa, args.deb)
