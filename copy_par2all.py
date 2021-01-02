#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os

par_c=[
"par_dipl_syn.json",
"par_dipl_txt.json",
"par_inter_syn.json",
"par_inter_txt.json"
]

par_p=[
"par.json",
"par_syn.json",
"par_syn_pannel.json",
"par_syn_format.json",
"par_txt.json",
"par_txt_pannel.json",
"par_txt_format.json",
"par_xml.json"
]

for p in par_c:
    fpar=f'cnf/{p}'
    ftor=fpar.replace('par','tor')
    ftou=fpar.replace('par','tou')
    fven=fpar.replace('par','ven')
    with open(fpar,'r') as f:
        txt=f.read()
    s=txt.replace('par','tor')
    s=s.replace('html_torams','html_params')
    with open(ftor,"w+") as f:
        f.write(s)
    s=txt.replace('par','tou')
    s=s.replace('html_touams','html_params')
    with open(ftou,"w+") as f:
        f.write(s)
    s=txt.replace('par','ven')
    s=s.replace('html_venams','html_params')
    with open(fven,"w+") as f:
        f.write(s)
for p in par_p:
    fpar=f'prj/{p}'
    ftor=fpar.replace('par','tor')
    ftou=fpar.replace('par','tou')
    fven=fpar.replace('par','ven')
    with open(fpar,'r') as f:
        txt=f.read()
    s=txt.replace('par','tor')
    s=s.replace('tor_sub','par_sub')
    s=s.replace('tor_name','par_name')
    s=s.replace('torams','params')
    with open(ftor,"w+") as f:
        f.write(s)
    s=txt.replace('par','tou')
    s=s.replace('tou_sub','par_sub')
    s=s.replace('tou_name','par_name')
    s=s.replace('touams','params')
    with open(ftou,"w+") as f:
        f.write(s)
    s=txt.replace('par','ven')
    s=s.replace('ven_sub','par_sub')
    s=s.replace('ven_name','par_name')
    s=s.replace('venams','params')
    with open(fven,"w+") as f:
        f.write(s)
