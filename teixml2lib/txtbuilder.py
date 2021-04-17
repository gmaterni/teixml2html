#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pdb import set_trace
import os
import pprint
from teixml2lib.ualog import Log
from teixml2lib.uainput import Inp
import sys
import re

def pp(data):
    return  pprint.pformat(data, indent=2, width=40)

class TxtBuilder:

    def __init__(self):
        self.log = Log("w")
        self.log.open("log/log/txtbuilder.log", 0)
        self.logerr = Log("a")
        self.logerr.open("log/txtbuilder.ERR.log", 1)
        self._data_lst=[]
        self._data_txt_lst=[]
        self._data_span_lst=[]
        self._from_to_lst=[]
        self._txt_rows=[]
        self.up=True
        self.w_liv=100
            
    def w_num(self,id):
        p =id.find('w')
        if p < 0:
            return -1
        return int(id[p+1:])

    def set_data_txt(self,i,d):
        txt_id = d["id"]
        is_parent = d["is_parent"]
        txt_items = d["items"]
        txt_liv = d["liv"]
        txt_tag = d['tag']
        txt_text = d['text']
        txt_tail = d['tail']

        c_keys = d['c_keys']
        c_attrs = d['c_attrs']
        c_text = d['c_text']
        c_params = d['c_params']
        c_paren = d['c_parent']
        d['t_i']=i
        flag=False
        sp='' 
        ln=False

        if txt_tag=='w':
            flag=True
            if self.w_num(txt_id)>1:
                sp=' '
            self.w_liv=txt_liv
        elif txt_tag=='pc':
            flag=True
            if txt_text.strip() in ['.','!','?']:
                self.up=True
        else:
            if txt_liv >= self.w_liv:
                flag=True
            else:
                flag=False
            if txt_tag=='l':
                ln=True

        d['t_flag']=flag
        d['t_sp']=sp
        d['t_ln']=ln
        if self.up and flag and txt_tag!='pc':
            d['t_up']=True
            self.up=False 

    def fill_span_list(self):
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
            self._from_to_lst.append(item)

    def set_from_to(self,i):
        from_to=self._from_to_lst[i]
        id_from = from_to['id0']
        if id_from=='':
            return
        id_to = from_to['id1']
        if id_to=='':
            return
        span_type = from_to['type']
        for i in range (0,len(self._data_txt_lst)):
            data_txt=self._data_txt_lst[i]
            id=data_txt['id']
            if id=='':
                continue
            if id_from == id:
                if span_type=="monologue":
                    data_txt['t_start']='['
                elif span_type=="directspeech":
                    data_txt['t_start']='{'
            elif id_to == id:
                if span_type=="monologue":
                    data_txt['t_end']=']'
                elif span_type=="directspeech":
                    data_txt['t_end']='}'

    def build_txt_rows(self):
        self._txt_rows=[]
        words=[]
        for d in self._data_txt_lst:
            if d['t_start']!='':
                words.append(d['t_start'])

            w=d['t_sp']
            if w!='':
                words.append(w)

            w=f"{d['text']}{d['tail']}"
            w=w.strip()
            if w !='':        
                w=w.lower()
                if d['t_up']:
                    w=w.capitalize()
                words.append(w)

            w=d['t_end']
            if w!='':
                words.append(w)

            if d['t_ln']:
                row=''.join(words)
                self._txt_rows.append(row)
                words=[]

    def text_adjust(self):
        for i,rw in enumerate(self._txt_rows):
            rw=re.sub(r" ,", ", ",rw)
            rw=re.sub(r" ;", "; ",rw)
            rw=re.sub(r" \.", ". ",rw)

            rw=re.sub(r'\[ ', ' "',rw)
            rw=re.sub(r'\]', '"',rw)
            rw=re.sub(r'{ ', ' "',rw)
            rw=re.sub(r'}', '"',rw)
            
            rw=re.sub(r"\s{2,}", " ",rw)
            self._txt_rows[i]=rw.strip()

    def elab(self):
        for data_txt in self._data_lst:
            if data_txt['tag']=='span':
                self._data_span_lst.append(data_txt)
            else:
                self._data_txt_lst.append(data_txt)
        #
        self.fill_span_list()
        
        for i,data_txt in enumerate(self._data_txt_lst):
            self.set_data_txt(i,data_txt)
        #
        for i in range (0,len(self._from_to_lst)):
            self.set_from_to(i)
        #
        self.build_txt_rows()
        self.text_adjust()

    def add(self,data):
        self._data_lst.append(data)
     
    @property
    def data_lst(self):
        return self._data_lst

    @property
    def data_txt_lst(self):
        return self._data_txt_lst

    @property
    def data_span_lst(self):
        return self._data_span_lst

    @property
    def from_to_lst(self):
        return self._from_to_lst

    @property
    def txt_rows(self):
        return self._txt_rows
    
    @property
    def txt(self):
        s=os.linesep.join(self.txt_rows)
        return s
