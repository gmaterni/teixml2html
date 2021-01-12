#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
import pathlib as pl


par1_c=[
"par1_dipl_syn.json",
"par1_dipl_txt.json",
"par1_inter_syn.json",
"par1_inter_txt.json"
]

def files_of_dir(d, e):
    p = pl.Path(d)
    fs = sorted(list(p.glob(e)))
    return fs

def one2all(dr,man):
    ptrn=f'{man}*.*'
    one_lst=files_of_dir(dr,ptrn)
    for x in one_lst:
        print(x)
    #
     
    """
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
        """

if __name__ == "__main__":
    dr=sys.argv[1]
    man=sys.argv[2]
    one2all(dr,man)