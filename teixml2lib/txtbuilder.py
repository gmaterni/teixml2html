#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pdb import set_trace
import os
import pprint
from teixml2lib.ualog import Log
from teixml2lib.uainput import Inp
import teixml2lib.prndata as pd
import sys
import re


def pp(data):
    return pprint.pformat(data, indent=2, width=40)


inp = Inp()
inp.set_liv(1)

"""
i|c+#affr|span||class:diacr_int|%%text%%|c:ç
i|c+#ced-dipl|span||class:diacr_int|%%text%%|ç:ç
i|c+#diacr-desamb|span||class:diacr_int|%%text%%|a:à,o:ò,u:ù,e:è,A:à,E:è,I:ì,O:ò,U:ù
i|c+#e-ton|span||class:diacr_int|%%text%%|e:é
i|c+#hiat|span||class:diacr_int|%%text%%|i:ï,u:ü,e:ë
i|c+#lram-c|span||class:ramis_int|%%text%%|V:v,J:j,u:v,i:j
i|c+#lram-v|span||class:ramis_int|%%text%%|V:u,v:u,j:i,J:i
i|c+e-ton|span||class:diacr_int|%%text%%|e:é
"""
RAMIS = [
    "#affr|c:ç",
    "#ced-dipl|ç:ç",
    "#diacr-desamb|a:à,o:ò,u:ù,e:è,A:à,E:è,I:ì,O:ò,U:ù",
    "#e-ton|e:é",
    "#hiat|i:ï,u:ü,e:ë",
    "#lram-c|V:v,J:j,u:v,i:j",
    "#lram-v|V:u,v:u,j:i,J:i",
    "e-ton|e:é"
]

# APOSTR="`"
ELIS = "’"
ENCL = "·"
NAMES_UP = ['forename', 'addname', 'name']
START = 't_start'
END = 't_end'
MONOLOG = 'monologue'
DIRECT = 'directspeech'


class TxtBuilder:

    def __init__(self):
        self.log = Log("w")
        self.log.open("log/txtbuilder.log", 0)
        self.logerr = Log("a")
        self.logerr.open("log/txtbuilder.ERR.log", 1)
        self.data_lst = []
        self.data_txt_lst = []
        self.data_span_lst = []
        self.from_to_lst = []
        self.txt_rows = []
        self.up = True
        self.w_liv = 100
        self.trace = False
        self.ramis=self.set_ramis_dict()

    def set_ramis_dict(self):
        js={}
        for r in RAMIS:
            k,v=r.split('|')
            js[k]={}
            ls=v.split(',')
            for xy in ls:
                x,y=xy.split(':')
                js[k][x]=y
        return js

    def get_ramis(self,key,ch):
        js=self.ramis.get(key,None)
        if js is None:
            return f"ERR{key}"
        r=js.get(ch,None)
        if r is None:
            return f"ERR{ch}"
        return r

    def fill_from_to_list(self):
        for data_span in self.data_span_lst:
            x_items = data_span.get('items', {})
            x_from = x_items.get('from', None)
            x_to = x_items.get('to', None)
            x_type = x_items.get('type', None)
            if x_from is None or x_to is None or x_type is None:
                self.logerr.log("fill_span_list ERROR.").prn()
                self.logerr.log(pp(data_span)).prn()
                sys.exit(1)
            item = {
                "id0": x_from,
                "id1": x_to,
                "type": x_type
            }
            self.from_to_lst.append(item)

    def from_to_set_data_txt(self):
        for i in range(0, len(self.from_to_lst)):
            from_to = self.from_to_lst[i]
            id_from = from_to['id0'].strip()
            id_to = from_to['id1'].strip()
            span_type = from_to['type'].strip()
            err = 0
            if id_from == '':
                err = 1
            if id_to == '':
                err = 2
            if err == 1:
                self.logerr.log(f"ERROR from is null. to:{id_to}.")
            elif err == 2:
                self.logerr.log(f"ERROR from={id_from}  to is null.")
            for i in range(0, len(self.data_txt_lst)):
                data_txt = self.data_txt_lst[i]
                id = data_txt['id']
                if id == '':
                    continue
                if id_from == id:
                    if span_type == MONOLOG:
                        if err == 0:
                            data_txt[START] = '['
                        else:
                            data_txt[START] = '[ERR '
                    elif span_type == DIRECT:
                        if err == 0:
                            data_txt[START] = '{'
                        else:
                            data_txt[START] = '{ERR '
                elif id_to == id:
                    if span_type == MONOLOG:
                        if err == 0:
                            data_txt[END] = ']'
                        else:
                            data_txt[END] = ' ERR]'
                    elif span_type == DIRECT:
                        if err == 0:
                            data_txt[END] = '}'
                        else:
                            data_txt[END] = ' ERR}'

    # def w_num(self, id):
    #     p = id.find('w')
    #     if p < 0:
    #         return -1
    #     return int(id[p+1:])

    def set_data_txt_list(self):
        """setta t_data utilizzano xml_data e csv_data
        """
        t_up = False
        sic = False
        w_num = 0
        for i, d in enumerate(self.data_txt_lst):
            #id = d["id"]
            liv = d["liv"]
            tag = d['tag'].lower().strip()
            d['tag'] = tag
            text = d['text'].strip()
            d['t_i'] = i
            sp = ''
            ln = False

            if text != '':
                if t_up:
                    self.data_txt_lst[i]['t_up'] = True
                    t_up = False
                if sic:
                    self.data_txt_lst[i]['text'] = ''
                    sic = False

            if tag == 'w':
                sp = ' '
                self.w_liv = liv
            elif tag == 'pc':
                if text in ['.', '!', '?']:
                    t_up = True
            elif tag in NAMES_UP:
                t_up = True
            elif tag in ['lg']:
                t_up = True
            elif tag == 'del':
                self.data_txt_lst[i]['text'] = ''
                self.data_txt_lst[i]['tail'] = ''
            elif tag == 'sic':
                sic = True
            elif tag == 'l':
                ln = True
            d['t_sp'] = sp
            d['t_ln'] = ln

    def is_in_xml_items(self, items, key, val):
        v = items.get(key, '')
        v = v.replace('#', '').strip()
        return v == val

    def build_txt_rows(self):
        """crea le righe di testo self._txt_rows
        utilizzando data_text=xml_data + csv_data + t_data
        """
        self.txt_rows = []
        words = []
        for i, d in enumerate(self.data_txt_lst):
            id = d['id']
            tag = d['tag'].strip()
            text = d['text'].strip()
            tail = d['tail'].strip()
            items = d['items']
            t_start = d['t_start']
            t_sp = d['t_sp']
            t_up = d['t_up']
            t_end = d['t_end']
            t_ln = d['t_ln']

            if tag == 'c':
                if len(text)==1:
                    k=items.get('ana',None)
                    if k is not None:
                        r=self.get_ramis(k,text)
                        text=r

            elif tag == 'w':
                # els
                if self.is_in_xml_items(items, 'ana', 'elis'):
                    text = f'{text}{ELIS}'
                    self.data_txt_lst[i+1]['t_sp'] = ''
                # encl
                if self.is_in_xml_items(items, 'ana', 'encl'):
                    text = f'{ENCL}{text} '
                    t_sp = ''

            if t_sp != '':
                words.append(t_sp)

            if t_start != '':
                words.append(t_start)

            if t_up:
                text = text.capitalize()
            else:
                text = text.lower()
            tail = tail.lower()

            w = f"{text}{tail}"
            if w != '':
                words.append(w)

            if t_end != '':
                words.append(t_end)

            if t_ln:
                row = ''.join(words)
                self.txt_rows.append(row)
                words = []
        row = ''.join(words).strip()
        self.txt_rows.append(row)

    def text_adjust(self):
        VIRG = '"'
        for i, rw in enumerate(self.txt_rows):
            rw = re.sub(r" ,", ", ", rw)
            rw = re.sub(r" ;", "; ", rw)
            rw = re.sub(r" \.", ". ", rw)

            rw = re.sub(r'\[\s*', ' "', rw)
            rw = re.sub(r'\]', '" ', rw)
            rw = re.sub(r'{\s*', ' "', rw)
            rw = re.sub(r'}', '" ', rw)
            rw = rw.replace(f"{ELIS} ", ELIS)
            rw = re.sub(r"\s{2,}", " ", rw)
            self.txt_rows[i] = rw.strip()

    def elab(self):
        for data in self.data_lst:
            if data['tag'] == 'span':
                self.data_span_lst.append(data)
            else:
                self.data_txt_lst.append(data)
        # popola la lista con gli id from to
        self.fill_from_to_list()
        # completa gli elemnti di data_txt_lst
        self.set_data_txt_list()
        # setta start ed end in datat_tx
        self.from_to_set_data_txt()
        # cra le righe di testo
        self.build_txt_rows()
        # sistema le righe du testo
        self.text_adjust()

    def add(self, data):
        self.data_lst.append(data)

    @property
    def txt(self):
        s = os.linesep.join(self.txt_rows)
        return s
