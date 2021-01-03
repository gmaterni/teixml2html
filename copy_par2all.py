#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os

par1_c=[
"par1_dipl_syn.json",
"par1_dipl_txt.json",
"par1_inter_syn.json",
"par1_inter_txt.json"
]

par1_p=[
"par1.json",
"par1_syn.json",
"par1_syn_pannel.json",
"par1_syn_format.json",
"par1_txt.json",
"par1_txt_pannel.json",
"par1_txt_format.json",
"par1_xml.json"
]

for p in par1_c:
    fpar=f'cnf/{p}'
    ftor=fpar.replace('par1','tor1')
    ftou=fpar.replace('par1','tou1')
    fven=fpar.replace('par1','ven1')
    with open(fpar,'r') as f:
        txt=f.read()

    s=txt.replace('par1','tor1')
    with open(ftor,"w+") as f:
        f.write(s)

    s=txt.replace('par1','tou1')
    with open(ftou,"w+") as f:
        f.write(s)

    s=txt.replace('par1','ven1')
    with open(fven,"w+") as f:
        f.write(s)

for p in par1_p:
    fpar=f'prj/{p}'
    ftor=fpar.replace('par1','tor1')
    ftou=fpar.replace('par1','tou1')
    fven=fpar.replace('par1','ven1')
    with open(fpar,'r') as f:
        txt=f.read()

    s=txt.replace('par1','tor1')
    with open(ftor,"w+") as f:
        f.write(s)

    s=txt.replace('par1','tou1')
    with open(ftou,"w+") as f:
        f.write(s)

    s=txt.replace('par1','ven1')
    with open(fven,"w+") as f:
        f.write(s)
