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
from teixml2lib.readtxtconf import read_tag_csvf
from teixml2lib.readjson import read_json
from teixml2lib.uainput import Inp
from teixml2lib.ualog import Log
from teixml2lib import file_utils as fu

__date__ = "17-04-2021"
__version__ = "0.1.1"
__author__ = "Marta Materni"


def pp(data):
    if data is None:
        return ""
    s = pprint.pformat(data, indent=2, width=40)
    return s


log = Log("w")
logerr = Log("a")

inp = Inp()


class Xml2Txt:

    def __init__(self):
        log.open("log/teixml2txt.log", 0)
        logerr.open("log/teixml2txt.ERR.log", 1)

        self.xml_path = ''
        self.txt_path = None
        self.txt_cfg = None
        self.txt_tag_cfg = None
        self.txt_builder = None

        self.x_data_dict = {}
        
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
        tag = nd.tag
        tag = tag if type(nd.tag) is str else "XXX"
        p = tag.rfind('}')
        if p > 1:
            logerr.log("ERROR in  xml")
            logerr.log(nd.tag)
            sys.exit(1)
        return tag.strip()

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
        return {
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

    def get_data_row_txt_csv(self, x_data):
        xml_tag = x_data['tag']
        row_data = self.txt_tag_cfg.get(xml_tag, None)
        if row_data is None:
            row_data = self.txt_tag_cfg.get('x', {})
            csv_tag = xml_tag
            self.csv_tag_ctrl = f'_x_{csv_tag}'
        else:
            tag = row_data.get('tag', f"_x_{xml_tag}")
            p = tag.find('+')
            if p > -1:
                x_items = x_data['items']
                lsk = tag.split('+')[1:]
                lsv = [x_items[k] for k in lsk if k in x_items.keys()]
                attrs_val = '+'.join(lsv)
                csv_tag = xml_tag+'+'+attrs_val
                row_data = self.txt_tag_cfg.get(csv_tag, None)
                if row_data is None:
                    row_data = self.txt_tag_cfg.get('x+y', None)
                    self.csv_tag_ctrl = f'_xy_{csv_tag}'
                else:
                    self.csv_tag_ctrl = csv_tag
            else:
                csv_tag = xml_tag
                self.csv_tag_ctrl = csv_tag
        self.x_data_dict[csv_tag] = x_data
        return row_data

    def build_txt_data(self, nd):
        x_data = self.get_node_data(nd)
        c_data = self. get_data_row_txt_csv(x_data)
        txt_data = {
            'id': x_data.get('id',0),
            'is_parent':x_data.get('is_parent',False),
            'items': x_data.get('items',{}),
            'liv': x_data.get('liv',0),
            'tag': x_data.get('tag',''),
            'text': x_data.get('text',''),
            'tail': x_data.get('tail',''),
            'val': x_data.get('val',''),

            #'c_xml_tag': c_data.get('xml_tag',''),
            # 'c_tag': c_data.get('tag',''),
            'c_keys':c_data.get('keys',[]),
            'c_attrs':c_data.get('',{}),
            'c_text': c_data.get('text',''),
            'c_params': c_data.get('params',''),
            'c_parent': c_data.get('parent',''),

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

    def prn_data(self,d):
        txt_id = d['id']
        is_parent = d['is_parent']
        txt_items = d['items']
        txt_liv = d['liv']
        txt_tag = d['tag']
        txt_text = d['text']
        txt_tail = d['tail']
        
        #c_xml_tag = txt_data['c_xml_tag']
        # c_tag = txt_data['c_div']
        c_keys = d['c_keys']
        c_attrs = d['c_attrs']
        c_text = d['c_text']
        c_params = d['c_params']
        c_parent = d['c_parent']

        t_i = d['t_i']
        t_type = d['t_type']
        t_up = d['t_up']
        t_start = d['t_start']
        t_end = d['t_end']
        t_sp = d['t_sp']
        t_ln = d['t_ln']
        t_flag = d['t_flag']
        
        log.log("--- txt_data").prn()
        log.log(f"id: {txt_id}").prn()
        log.log(f"is_parent: {is_parent}").prn()
        log.log(f"liv: {txt_liv     }").prn()
        log.log(f"txt_items: {txt_items}").prn()
        log.log(f"txt_tag: {txt_tag}").prn()
        log.log(f"txt_text: {txt_text}").prn()
        log.log(f"txt_tail: {txt_tail}").prn()

        log.log("--- c_data").prn()
        #log.log(f"c_xml_tag: {c_xml_tag}").prn()
        # log.log(f"c_tag: {c_tag}").prn()
        log.log(f"c_keys: {c_keys}").prn()
        log.log(f"c_attrs: {c_attrs}").prn()
        log.log(f"c_text: {c_text}").prn()
        log.log(f"c_params: {c_params}").prn()
        log.log(f"c_paren: {c_parent}").prn()

        log.log("--- t_data").prn()
        log.log(f"t_i: {t_i}").prn()
        log.log(f"t_type: {t_type}").prn()
        log.log(f"t_up: {t_up}").prn()
        log.log(f"t_start: {t_start}").prn()
        log.log(f"t_end: {t_end}").prn()
        log.log(f"t_sp: {t_sp}").prn()
        log.log(f"t_ln: {t_ln}").prn()
        log.log(f"t_flag: {t_flag}").prn()


    def prn_data_lst(self):
        log.log('===============').prn()
        for d in self.txt_builder._data_lst:
            self.prn_data(d)
            log.log('').prn()
            inp.inp('!')


    def read_conf(self, json_path):
        try:
            self.txt_cfg = read_json(json_path)
            csv_path = self.txt_cfg.get("txt_tag_file", None)
            log.log(f"csv_path:{csv_path}")
            if csv_path is None:
                raise Exception("ERROR txt.csv is null.")
            self.txt_tag_cfg = read_tag_csvf(csv_path, "i:txt")
        except Exception as e:
            logerr.log("ERROR: read_conf())")
            logerr.log(e)
            sys.exit(1)
    
    def write_txt(self,
                  xml_path='',
                  txt_path='',
                  json_path='',
                  write_append = 'w',
                  debug_liv = '0'):
        try:
            debug_liv=2
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
                logerr.log("ERROR teixml2txt.py write_txt() parse_xml")
                logerr.log(e)
                sys.exit(1)
            self.read_conf(json_path)
            self.txt_builder=TxtBuilder()
            ########################
            for nd in xml_root.iter():
                txt_data=self.build_txt_data(nd)
                #self.prn_txt_data(txt_data)
                #inp.inp('!')
                self.txt_builder.add(txt_data)
            ########################
            self.txt_builder.elab()           
            self.prn_data_lst()
            txt=self.txt_builder.txt
            #print(txt)
            fu.make_dir_of_file(self.txt_path)
            with open(self.txt_path, write_append) as f:
                f.write(txt)
            fu.chmod(self.txt_path)
        except Exception as e:
            logerr.log("ERROR teixml2txt.py write_html()")
            logerr.log(e)
            ou=StringIO()
            traceback.print_exc(file = ou)
            st=ou.getvalue()
            ou.close()
            logerr.log(st)
            sys.exit(1)
        return self.txt_path

def do_mauin(xml, txt, conf, wa = 'w', deb = False):
    Xml2Txt().write_txt(xml, txt, conf, wa, deb)

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
    parser.add_argument('-c',
                        dest = "cfg",
                        required = True,
                        metavar = "",
                        help = "-c <file_conf.json")
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
    do_mauin(args.xml, args.txt, args.cfg, args.wa, args.deb)
