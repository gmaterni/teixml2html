#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pdb import set_trace
import json
import os
import pprint
import sys
import pathlib as pl
from ualog import Log


def pp(data):
    if data is None:
        return ""
    s = pprint.pformat(data, indent=2, width=120)
    return s+os.linesep


__date__ = "15-01-2021"
__version__ = "0.3.2"
__author__ = "Marta Materni"

logerr = Log("a")
loginfo = Log("a")


def prn_es():
    js = {
        "exe": [
            [
                "teimxml.py",
                "-i prova01.txt",
                "-t tags01.csv",
                "-o prova01_v.txt"
            ]
        ],
        "exe.2": [
            "teimlineword.py -i prova01_v.txt -o prova01_vlw.xml",
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
                "-cd cnf/par_dipl_syn.json",
                "-ci cnf/par_inter_syn.json"
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

class PrjMgr:

    def __init__(self):
        logerr.open("log/prjmgr.ERR.log", 1)
        loginfo.open("log/prjmgr.log", 1)


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

    def include_files(self, include):
        """nel file host sostitusce ogni parametro
        con il file ad esso collegato

        Args:
            js (dict): "include". ramo del project
        """
        loginfo.log(os.linesep, ">> include")
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
                loginfo.log(f"{param}: {path}")
                with open(path, "rt") as f:
                    txt = f.read()
                host = host.replace(param, txt)
            #
            for key_val in param_lst:
                key, val = self.kv_split(key_val, '|')
                loginfo.log(f"{key}: {val}")
                host = host.replace(key, val)
            #
            with open(file_dest, "w+") as f:
                f.write(host)
            os.chmod(file_dest, 0o666)
        except Exception as e:
            logerr.log("include")
            logerr.log(e)
            sys.exit(1)

    def execute_files_of_dir(self, exe_dir):
        loginfo.log(os.linesep, ">> exe_dir")
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
                    loginfo.log(x)
                    r = os.system(x)
                    if r != 0:
                        raise Exception(f"ERROR execute:{x}")
        except Exception as e:
            logerr.log("exe_dir")
            logerr.log(e)
            logerr.log(pp(exe_dir))
            sys.exit(1)

    def remove_files_of_dir(self, remove_dir):
        loginfo.log(os.linesep, ">> remove_dir")
        try:
            for de in remove_dir:
                loginfo.log(de)
                dr = de.get('dir')
                ptrn = de.get('pattern')
                files = self.files_of_dir(dr, ptrn)
                for f in files:
                    loginfo.log(f)
                    os.remove(f)
        except Exception as e:
            logerr.log("remove_dir")
            logerr.log(e)
            logerr.log(pp(remove_dir))
            sys.exit(1)

    def merge_files_of_list(self, merge_files):
        loginfo.log(os.linesep, ">> merge_files")
        out = self.get(merge_files, "out_path")
        files = self.get(merge_files, "files")
        fout = open(out, "w+")
        for f in files:
            loginfo.log(f)
            with open(f, "rt") as f:
                txt = f.read()
            fout.write(txt)
            fout.write(os.linesep)
        fout.close()
        loginfo.log(out)
        os.chmod(out, 0o666)

    def merge_files_of_dir(self, merge_dir):
        loginfo.log(os.linesep, ">> merge_dir")
        try:
            dr = self.get(merge_dir, 'dir')
            ptrn = self.get(merge_dir, 'pattern')
            out_path = self.get(merge_dir, 'out_path')
            files = self.files_of_dir(dr, ptrn)
            file_out = open(out_path, "w")
            for fpath in files:
                loginfo.log(fpath)
                with open(fpath, "rt") as f:
                    txt = f.read()
                file_out.write(txt)
                file_out.write(os.linesep)
            file_out.close()
            os.chmod(out_path, 0o666)
            loginfo.log(out_path)
        except Exception as e:
            logerr.log("merge_dir")
            logerr.log(e)
            logerr.log(pp(merge_dir))
            sys.exit(1)

    def execute_list_progs(self, exe):
        loginfo.log(os.linesep, ">> exe")
        try:
            for x in exe:
                x = self.list2str(x)
                loginfo.log(x)
                r = os.system(x)
                if r != 0:
                    raise Exception(str(r))
        except Exception as e:
            logerr.log("exe")
            logerr.log(e)
            logerr.log(pp(exe))
            sys.exit(1)

    def copy_file(self, copy_file):
        loginfo.log(os.linesep, ">> copy_file")
        try:
            in_path = self.get(copy_file, 'in_path')
            out_path = self.get(copy_file, 'out_path')
            aw = self.get(copy_file, "aw")
            loginfo.log(in_path)
            with open(in_path, "rt") as f:
                text = f.read()
            with open(out_path, aw) as f:
                f.write(text)
                if aw == 'a':
                    f.write(os.libnesep)
            os.chmod(out_path, 0o666)
            loginfo.log(out_path)
        except Exception as e:
            logerr.log("copy_file")
            logerr.log(e)
            logerr.log(pp(copy_file))
            sys.exit(1)

    def write_text(self, write_text):
        loginfo.log(os.linesep, ">> write_text")
        try:
            text = self.get(write_text, 'text')
            out_path = self.get(write_text, 'out_path')
            aw = self.get(write_text, "aw")
            with open(out_path, aw) as f:
                f.write(text)
                if aw == 'a':
                    f.write(os.libnesep)
            os.chmod(out_path, 0o666)
            loginfo.log(out_path)
        except Exception as e:
            logerr.log("write_text")
            logerr.log(e)
            logerr.log(pp(write_text))
            sys.exit(1)


    def parse_json(self, js):
        for k, v in js.items(): 
            # accetta  tag del tipo exe.1 exe.2 ..
            k=k.split('.')[0]
            if k=="exe":
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
            else:
                logerr.log(f"ERROR option:{k} not implemented")
                    
        
    def parse_file(self, in_path):
        try:
            with open(in_path, "r") as f:
                txt = f.read()
            js = json.loads(txt)
        except Exception as e:
            logerr.log("json ERROR")
            logerr.log(e)
            sys.exit(1)
        self.parse_json(js)



if __name__ == "__main__":
    if len(sys.argv) == 1:
        prn_es()
        sys.exit()
    src_path=sys.argv[1]
    PrjMgr().parse_file(src_path)
