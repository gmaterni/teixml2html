#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from os.path import isdir
import sys
from pdb import set_trace
import os
import stat
import shutil

def chmod(path):
    os.chmod(path, stat.S_IRWXG + stat.S_IRWXU + stat.S_IRWXO)

def copy_xml(name):
    dir_xml=f"{name}_xml/xml"
    dir_html=f"{name}_html/xml"
    print(name)
    print(dir_xml)
    print(dir_html)
    print("")
    if not os.path.isdir(dir_xml):
        print(f"{dir_xml} Not found.")
        return
    if not os.path.isdir(dir_html):
        print(f"{dir_html} Not found.")
        return
    for f in os.listdir(dir_xml):
        name=os.path.basename(f)
        if name.find(".xml")<0:
            continue
        path_src = os.path.join(dir_xml, name)
        path_dst = os.path.join(dir_html, name)
        print(path_src)
        print(path_dst)
        print("")
        shutil.copyfile(path_src,path_dst)
        chmod(path_dst)

if __name__ == "__main__":
    le=len(sys.argv)
    if le ==2 :
        name=sys.argv[1]
        copy_xml(name)        
    else:
        print("copy_xml.py <nome progetto>")
        print("es. per  flori_xml,flori_html")
        print("digitare copy_xml.py flori")
