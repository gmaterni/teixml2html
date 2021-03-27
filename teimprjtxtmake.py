#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
import stat
import pathlib as pl
from pdb import set_trace
from teimx2hlib import template_txt_prj
import json

__date__ = "01-03-2021"
__version__ = "0.1.0"
__author__ = "Marta Materni"

help = """
prjmgr.py prj/<prj.json>

witness_checkover.json
witness_checktxt.json
witness_rmovelog.json
witness_merge.json
witness_txt.json
witness_xml.json
witness.json
-------------------------------
prjmgr.py witness_prj/<prj.json>

text_checkover.json
text_checktxt.json
text_removelog.json
text_txt.json
text_lineword.json
text_note.json
text_over.json
text.json
"""

TEIM_WORK = "teim_work"
PRJ = "prj"
LOG = "log"
CFG = "cfg"
PRJ_CFG = "prj_cfg"
XML = "xml"
TXT = "txt"
WITNESS = "witness"


class TeimPrjTxtMake(object):

    def __init__(self,
                 work_name,
                 witness_name):
        # dir virtuali  template
        self.tmpl_work = TEIM_WORK
        self.tmpl_prj = os.path.join(self.tmpl_work, PRJ)
        self.tmpl_prj_cfg = os.path.join(self.tmpl_work, PRJ_CFG)
        # nomi work+witness+text
        self.work_name = work_name
        self.dir_work = work_name
        self.witness_name = witness_name
        #self.witness_log_x = f"{witness_name}_log"
        # dir progetto  work work/prj work/cfg work/log work/xml work/txt
        self.dir_prj = os.path.join(self.dir_work, PRJ)
        self.dir_prj_cfg = os.path.join(self.dir_work, PRJ_CFG)
        self.dir_cfg = os.path.join(self.dir_work, CFG)
        self.dir_xml = os.path.join(self.dir_work, XML)
        self.dir_log = os.path.join(self.dir_work, LOG)
        self.dir_txt = os.path.join(self.dir_work, TXT)
        # dir txt/witness xml/witness
        self.dir_txt_witness_name = os.path.join(self.dir_txt,self.witness_name)
        self.dir_xml_witness_name = os.path.join(self.dir_xml,self.witness_name)

    def write_work_id(self):
        name_id="__prj__"
        text=f"{self.work_name}"
        path_id=os.path.join(self.dir_work,name_id)
        if os.path.exists(path_id):
            return
        with open(path_id,"w") as f:
            f.write(text)
        os.chmod(path_id, stat.S_IRWXG + stat.S_IRWXU + stat.S_IRWXO)


    def files_of_dir(self, path, ptrn):
        p = pl.Path(path)
        fs = sorted(list(p.glob(ptrn)))
        return fs

    def make_dir(self, dirname):
        if not os.path.isdir(dirname):
            print(dirname)
            os.mkdir(dirname)
            os.chmod(dirname, stat.S_IRWXG + stat.S_IRWXU + stat.S_IRWXO)

    #######################
    # copia dal template per progetti witntnes
    ######################
    def copy_prj_from_witness(self):
        for k, v in template_txt_prj.prj.items():
            prj = os.path.join(self.tmpl_prj, k)
            x = prj.replace(TEIM_WORK, self.work_name)
            x = x.replace(WITNESS, self.witness_name)
            prj_x = f"{x}.json"
            #
            src = json.dumps(v, indent=2)
            witness_src = src.replace(WITNESS, self.witness_name)
            with open(prj_x, "w") as f:
                f.write(witness_src)
            os.chmod(prj_x, stat.S_IRWXG + stat.S_IRWXU + stat.S_IRWXO)

    #######################
    # copia dal template per configurazione witntnes
    ######################
    def copy_prj_cfg_from_witness(self):
        for k, v in template_txt_prj.prj_cfg.items():
            prj = os.path.join(self.tmpl_prj_cfg, k)
            x = prj.replace(TEIM_WORK, self.work_name)
            x = x.replace(WITNESS, self.witness_name)
            prj_x = f"{x}.json"
            #
            src = json.dumps(v, indent=2)
            witness_src = src.replace(WITNESS, self.witness_name)
            with open(prj_x, "w") as f:
                f.write(witness_src)
            os.chmod(prj_x, stat.S_IRWXG + stat.S_IRWXU + stat.S_IRWXO)


    def print_dir(self):
        print("======================")
        print(self.dir_work)
        print(self.dir_cfg)
        print(self.dir_prj)
        print(self.dir_prj_cfg)
        print(self.dir_xml)
        print(self.dir_txt)
        print(self.dir_log)

    def make_dirs(self):
        self.make_dir(self.dir_work)
        self.make_dir(self.dir_cfg)
        self.make_dir(self.dir_prj)
        self.make_dir(self.dir_prj_cfg)
        self.make_dir(self.dir_xml)
        self.make_dir(self.dir_txt)
        self.make_dir(self.dir_log)
        #
        self.make_dir(self.dir_txt_witness_name)
        self.make_dir(self.dir_xml_witness_name)
        # self.print_dir()
        self.copy_prj_from_witness()
        self.copy_prj_cfg_from_witness()
        self.write_work_id()

def do_main(work, witness):
    mk = TeimPrjTxtMake(work, witness)
    mk.make_dirs()

def do_main_csv(project):
    try:
        with open(project, "r") as f:
            rows = f.readlines()
        for row in rows:
            sp = row.strip().split("|")
            if len(sp) < 2:
                return
            work, witness = sp
            do_main(work, witness)
    except Exception as e:
        print("EROROR in <name>_prj.csv")
        s = str(e)
        print(s)
        sys.exit(1)

def do_main_args(work, witness):
    if not os.path.isdir(work):
        print(f"{work} Not Found.")
        sys.exit(0)
    do_main(work, witness)

if __name__ == "__main__":
    le = len(sys.argv)
    if le == 2:
        csv = sys.argv[1]
        do_main_csv(csv)
    elif le == 3:
        work, witness = sys.argv[1:]
        do_main_args(work, witness)
    else:
        print("teimprjtxtmake.py <project.csv>")
        print("or if exists work")
        print("teimprjtxtmake.py <work> <witnes>")
        print(help)
        sys.exit(0)
