#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
from ualog import Log
import traceback 
# from pdb import set_trace
TAG_COL_NUM=7

logerr=Log()
logerr.open("log/readhtmlconf.err.log",1)

"""
xml_tag|tag|keys|attrs|text|params|parent
"""
def tags_cvs2json(csv):
    lsb=['','','','','','','']
    js = {}
    for row in csv:
        if row.strip()=="":
            continue
        try:
            row_data = {}
            row= row.replace(os.linesep,'')
            flds = row.split('|')
            if len(flds)<TAG_COL_NUM:
                le=len(flds)
                flds.extend(lsb[0:TAG_COL_NUM-le])
            xml_tag = flds[0]
            if xml_tag=='xml_tag':
                continue
            flds=[x.strip() for x in flds]
            # tag
            tag = flds[1]
            row_data['tag'] = tag
            #keys  []
            f = flds[2]
            if f != '':
                keys = f.split(',')
                row_data['keys'] = keys
            #attrs {}
            f = flds[3]
            if f != '':
                ls = f.split(',')
                attrs = {}
                for x in ls:
                    kv = x.split(':')
                    attrs[kv[0]] = kv[1]
                row_data['attrs'] = attrs
            # text=""
            f = flds[4]
            if f != '':
                row_data['text'] = f
            # params 
            f = flds[5]
            if f != '':
                ls = f.split(',')
                params = {}
                for x in ls:
                    kv = x.split(':')
                    params[kv[0]] = kv[1]
                row_data['params'] = params
            # parent
            f=flds[6]
            if f!='':
                row_data['parent']=f
            js[xml_tag] = row_data
        except Exception as e:
            s=traceback.format_exc()
            logerr.log("tag_csv2json")
            logerr.log(s)
            logerr.log(str(e))
            logerr.log(row)
            sys.exit()
    return js

def read_html_conf(csv_path):
    with open(csv_path, "r+") as f:
        csv = f.readlines()
    js = tags_cvs2json(csv)
    return js

