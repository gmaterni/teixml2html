#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#import os
import sys
from ualog import Log
import traceback 
import json

logerr=Log("a")
logerr.open("log/readjson.err.log",1)


def read_file_json(json_path):
    txt=''
    try:
        with open(json_path, "r") as f:
            txt = f.read()
        js = json.loads(txt)
    except Exception as e:
        s=traceback.format_exc()
        logerr.log("read_file_json()")
        logerr.log(s)
        logerr.log(str(e))
        logerr.log(txt)
        sys.exit()
    return js

def parse_json(js):
    for k,v in js.items():
        if isinstance(v,dict):
            parse_json(v)
            continue
        if isinstance(v,str):
            if v.find('$')> -1:
                path=v.replace('$',"")
                jsx=read_file_json(path)
                path=v.replace('$','')
                js[k]=jsx
                jsx=parse_json(jsx)
    return js


def read_json(json_path):
    js=read_file_json(json_path)
    js= parse_json(js)
    return js
    

#read_json("cnf/test0.json")