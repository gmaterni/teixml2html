#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
from ualog import Log
import traceback
# from pdb import set_trace
TAG_COL_NUM = 8

logerr = Log("w")
logerr.open("log/readhtmlconf.err.log", 1)


def t_split(s):
    sp = s.split(':')
    s0 = sp[0]
    le = len(sp)
    if le > 1:
        s1 = sp[1]
    else:
        s1 = ''
    return s0, s1

# d:syn
# SI  x, d, x:syn, d:syn
# NO  i, i:syn, x:pip, d:pip
# e    d, i, d:s. i:s
# t    x, d , i , x:s. d:s, i:s


def row_ok(e, t):
    if t == 'x' or t == e:
        return True
    if e.find(':') < 0:
        return False
    e0, e1 = t_split(e)
    if t == 'x' or t == e0:
        return True
    t0, t1 = t_split(t)
    if (t0 == 'x' or t0 == e0) and (t1 == e1):
        return True
    return False


# xml_tag|tag|keys|attrs|text|params|parent
def tags_cvs2json(csv, html_type):
    lsb = ['', '', '', '', '', '', '', '']
    js = {}
    # set_trace()
    for row in csv:
        if row.strip() == "":
            continue
        try:
            row_data = {}
            row = row.replace(os.linesep, '')
            flds = row.split('|')
            if len(flds) < TAG_COL_NUM:
                le = len(flds)
                flds.extend(lsb[0:TAG_COL_NUM-le])
            x = flds[0]
            if row_ok(html_type, x) is False:
                continue
            #
            flds = flds[1:]
            xml_tag = flds[0]
            if xml_tag == 'xml_tag':
                continue
            #
            flds = [x.strip() for x in flds]
            # tag
            tag = flds[1]
            row_data['tag'] = tag
            # keys  []
            f = flds[2]
            if f != '':
                keys = f.split(',')
                row_data['keys'] = keys
            # attrs {}
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
            f = flds[6]
            if f != '':
                row_data['parent'] = f
            js[xml_tag] = row_data
        except Exception as e:
            s = traceback.format_exc()
            logerr.log("tag_csv2json")
            logerr.log(s)
            logerr.log(str(e))
            logerr.log(row)
            sys.exit()
    return js


def read_html_conf(csv_path, html_type):
    with open(csv_path, "r+") as f:
        csv = f.readlines()
    js = tags_cvs2json(csv, html_type)
    return js
