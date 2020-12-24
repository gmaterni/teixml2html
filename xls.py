#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import pathlib as pl

def ls(d,e):
    p=pl.Path(d)
    if p.exists is False:
        print(f'{d} not found.')
        return[]
    fs=[x for x in p.glob(e)]
    return fs

    

fs=ls("html/par/txt/","*_F.html")

for x in fs:
    print(x)
