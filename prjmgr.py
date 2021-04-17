#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pdb import set_trace
import json
import os
import pprint
import sys
import pathlib as pl
from teixml2lib.ualog import Log
import stat

def pp(data):
    if data is None:
        return ""
    s = pprint.pformat(data, indent=2, width=80)
    return s+os.linesep

__date__ = "01-03-2021"
__version__ = "0.4.0"
__author__ = "Marta Materni"

def prn_es():
    js = {
        "log": "1",
        "exe": [
            [
                "teimxml.py",
                "-i prova01.txt",
                "-t tags01.csv",
                "-o prova01_v.txt"
            ]
        ],
        "exe.2": [
            "teimsetid.py -i prova01_v.txt -o prova01_vlw.xml",
            "xmllint --format prova01_vlw.xml -o prova01_vlwf.xml",
            "teimdict.py -i prova01.txt -o prova01_d.csv"
        ],
        "merge": {
            "out_path": "floripar.txt",
            "files": [
                "./eps/fl_par_ep12.txt",
                "./eps/fl_par_ep13.txt",
                "./eps/fl_par_ep14.txt",
                "./eps/fl_par_ep16.txt",
                "./eps/fl_par_ep17.txt",
            ]
        },
        "merge_dir": {
            "dir": "xml/par",
            "pattern": ".xml",
            "out_path": "floripar.txt"
        },
        "include": {
            "host": "html/txt_pannel.html",
            "dest": "html/par/txt/par.html",
            "params": [
                "MANO|par"
            ],
            "files": [
                "EPISODE_LIST_DIPL|html/par/txt/par_listd.html",
                "EPISODE_LIST_INTER|html/par/txt/par_listi.html"
            ]
        },
        "exe_dir": {
            "dir": "xml/par",
            "pattern": ".xml",
            "par_subst": ".xml|",
            "par_name": "$F",
            "exe_file": [
                "teixml2html_di_templ.py",
                "-i xml/par/$F.xml",
                "-o html/par/syn/$F.html",
                "-t html/syn_episode.html",
                "-cd cfg/par_dipl_syn.json",
                "-ci cfg/par_inter_syn.json"
            ]
        },
        "remove_dir": [
            {
                "dir": "html/par/syn",
                "pattern": "pa_list*.html"
            }
        ],
        "write_text": [
            {
                "text": "",
                "out_path": "",
                "aw": "a"
            }
        ],
        "copy_file": [
            {
                "in_path": "",
                "out_path": "",
                "aw": "a"
            }
        ],
    }
    s = pp(js)
    print(s)


class PrjMgr(object):

    def __init__(self):
        self.logerr = Log("a")
        self.log = Log("a")
        self.logerr.open("log/prjmgr.ERR.log", 1)
        self.log.open("log/prjmgr.log", 0)

    def kv_split(self, s, sep):
        sp = s.split(sep)
        s0 = sp[0].strip()
        s1 = ''
        if len(sp) > 1:
            s1 = sp[1].strip()
        return s0, s1

    def list2str(self, data):
        if isinstance(data, str):
            return data.strip()
        s = " ".join(data)
        return s.strip()

    def get(self, js, k):
        s = js.get(k, None)
        if s is None:
            raise Exception(f"{k} not found.{os.linesep}")
        return s

    def files_of_dir(self, d, e):
        p = pl.Path(d)
        if p.exists() is False:
            raise Exception(f'{d} not found.')
        fs = sorted(list(p.glob(e)))
        return fs

    def chmod(self, path):
        os.chmod(path, stat.S_IRWXG + stat.S_IRWXU + stat.S_IRWXO)

    def include_files(self, include):
        """nel file host sostitusce ogni parametro
        con il file ad esso collegato

        Args:
            js (dict): "include". ramo del project
        """
        self.log.log(os.linesep, ">> include")
        try:
            file_host = include.get("host", None)
            file_dest = include.get("dest", None)
            file_lst = include.get("files", [])
            param_lst = include.get("params", [])
            #
            with open(file_host, "rt") as f:
                host = f.read()
            #
            for param_path in file_lst:
                param, path = self.kv_split(param_path, '|')
                self.log.log(f"{param}: {path}")
                with open(path, "rt") as f:
                    txt = f.read()
                host = host.replace(param, txt)
            #
            for key_val in param_lst:
                key, val = self.kv_split(key_val, '|')
                self.log.log(f"{key}: {val}")
                host = host.replace(key, val)
            #
            with open(file_dest, "w+") as f:
                f.write(host)
            self.chmod(file_dest)
        except Exception as e:
            self.logerr.log("include")
            self.logerr.log(e)
            sys.exit(1)

    def execute_files_of_dir(self, exe_dir):
        self.log.log(">> exe_dir").prn()
        try:
            dr = self.get(exe_dir, 'dir')
            ptrn = self.get(exe_dir, 'pattern')
            exe_lst = self.get(exe_dir, 'exe_file')
            par_name = self.get(exe_dir, 'par_name')
            par_subst = self.get(exe_dir, 'par_subst')
            # replace par in par_name
            k, v = self.kv_split(par_subst, '|')
            files = self.files_of_dir(dr, ptrn)
            for f in files:
                file_name = os.path.basename(f)
                file_par = file_name.replace(k, v)
                for exe in exe_lst:
                    exe = self.list2str(exe)
                    x = exe.replace(par_name, file_par)
                    self.log.log(x)
                    r = os.system(x)
                    if r != 0:
                        raise Exception(f"execute:{x}")
        except Exception as e:
            self.logerr.log("ERROR","exe_dir")
            self.logerr.log(e)
            # self.logerr.log(pp(exe_dir))
            sys.exit(1)

    def remove_files_of_dir(self, remove_dir):
        self.log.log(">> remove_dir").prn()
        try:
            for de in remove_dir:
                self.log.log(de)
                dr = de.get('dir')
                ptrn = de.get('pattern')
                files = self.files_of_dir(dr, ptrn)
                for f in files:
                    self.log.log(f)
                    os.remove(f)
        except Exception as e:
            self.logerr.log("remove_dir")
            self.logerr.log(e)
            self.logerr.log(pp(remove_dir))
            sys.exit(1)

    def merge_files_of_list(self, merge_files):
        self.log.log(">> merge_files").prn()
        out = self.get(merge_files, "out_path")
        files = self.get(merge_files, "files")
        fout = open(out, "w+")
        for f in files:
            self.log.log(f)
            with open(f, "rt") as f:
                txt = f.read()
            fout.write(txt)
            fout.write(os.linesep)
        fout.close()
        self.log.log(out)
        self.chmod(out)

    def merge_files_of_dir(self, merge_dir):
        self.log.log(">> merge_dir").prn()
        try:
            dr = self.get(merge_dir, 'dir')
            ptrn = self.get(merge_dir, 'pattern')
            out_path = self.get(merge_dir, 'out_path')
            files = self.files_of_dir(dr, ptrn)
            file_out = open(out_path, "w")
            for fpath in files:
                self.log.log(fpath)
                with open(fpath, "rt") as f:
                    txt = f.read()
                file_out.write(txt)
                file_out.write(os.linesep)
            file_out.close()
            self.chmod(out_path)
            self.log.log(out_path)
        except Exception as e:
            self.logerr.log("merge_dir")
            self.logerr.log(e)
            self.logerr.log(pp(merge_dir))
            sys.exit(1)

    def execute_list_progs(self, exe):
        self.log.log( ">> exe").prn()
        try:
            for x in exe:
                x = self.list2str(x)
                self.log.log(x)
                r = os.system(x)
                if r != 0:
                    raise Exception(str(r))
        except Exception as e:
            self.logerr.log("exe")
            self.logerr.log(e)
            self.logerr.log(pp(exe))
            sys.exit(1)

    def copy_file(self, copy_file):
        self.log.log(">> copy_file").prn()
        try:
            for x in copy_file:
                in_path = self.get(x, 'in_path')
                out_path = self.get(x, 'out_path')
                aw = self.get(x, "aw")
                self.log.log(in_path)
                with open(in_path, "rt") as f:
                    text = f.read()
                with open(out_path, aw) as f:
                    f.write(text)
                    if aw == 'a':
                        f.write(os.linesep)
                self.chmod(out_path)
                self.log.log(out_path)
        except Exception as e:
            self.logerr.log("copy_file")
            self.logerr.log(e)
            self.logerr.log(pp(copy_file))
            sys.exit(1)

    def write_text(self, write_text):
        self.log.log(">> write_text").prn()
        try:
            text = self.get(write_text, 'text')
            out_path = self.get(write_text, 'out_path')
            aw = self.get(write_text, "aw")
            with open(out_path, aw) as f:
                f.write(text)
                if aw == 'a':
                    f.write(os.linesep)
            self.chmod(out_path)
            self.log.log(out_path)
        except Exception as e:
            self.logerr.log("write_text")
            self.logerr.log(e)
            self.logerr.log(pp(write_text))
            sys.exit(1)

    def parse_json(self, js):
        for k, v in js.items():
            # accetta  tag del tipo exe.1 exe.2 ..
            k = k.split('.')[0]
            if k == "exe":
                self.execute_list_progs(v)
            elif k == "merge_files":
                self.merge_files_of_list(v)
            elif k == "merge_dir":
                self.merge_files_of_dir(v)
            elif k == "include":
                self.include_files(v)
            elif k == "exe_dir":
                self.execute_files_of_dir(v)
            elif k == "remove_dir":
                self.remove_files_of_dir(v)
            elif k == "write_text":
                self.write_text(v)
            elif k == "copy_file":
                self.copy_file(v)
            elif k == "log":
                l = int(v)
                self.log.set_liv(l)
            else:
                self.logerr.log(f"ERROR option:{k} not implemented")

    def parse_file(self, in_path):
        try:
            with open(in_path, "r") as f:
                txt = f.read()
            js = json.loads(txt)
        except Exception as e:
            self.logerr.log("prjmgr.py json ERROR")
            self.logerr.log(e)
            sys.exit(1)
        self.parse_json(js)

    def parse_jsons(self,*js):
        lst=list(js)
        for j in lst:
            self.parse_json(j)

if __name__ == "__main__":
    if len(sys.argv) == 1:
        prn_es()
        sys.exit()
    pm=PrjMgr()
    lst = sys.argv[1:]
    for prj in lst:
        pm.parse_file(prj)
