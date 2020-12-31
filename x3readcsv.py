#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import pprint
from ualog import Log
from readhtmlconf import *

logconf1 = Log("w")
logconf2 = Log("w")

def pp(data):
    if data is None:
        return ""
    s = pprint.pformat(data, indent=2, width=120)
    return s+os.linesep


x=sys.argv[1]
html_type=x
x=x.replace(':','_')
logconf1.open(f"log/cnf{x}.json", 0)
logconf2.open(f"log/cnf{x}.txt", 0)
csv_path='cnf/html.csv'
#
# csv,js= read_html_conf(csv_path, html_type)
#############
with open(csv_path, "r+") as f:
    txt = f.read()
txt=txt.replace(f'\{os.linesep}','')
csv=txt.split(os.linesep)
js = tags_cvs2json(csv, html_type)
##############    
txt=pp(js).replace("'", '"')
logconf1.log(txt)
for r in csv:
    logconf2.log(r)

