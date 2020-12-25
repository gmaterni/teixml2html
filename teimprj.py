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


__date__ = "25-12-2020"
__version__ = "0.4.1"
__author__ = "Marta Materni"

logerr = Log("a")
loginfo = Log("a")


class PrjMgr:

    def __init__(self):
        logerr.open("log/teimprj.err.log", 1)
        loginfo.open("log/teimprj.log", 1)

    def get(self, js, k):
        s = js.get(k, None)
        if s is None:
            raise Exception(f"{k} not found.{os.linesep}")
        return s

    def list2str(self, x):
        if isinstance(x, str):
            return x
        s = " ".join(x)
        return s

    def files_of_dir(self, d, e):
        p = pl.Path(d)
        if p.exists() is False:
            raise Exception(f'{d} not found.')
        # fs = [x for x in p.glob(e)]
        fs=list(p.glob(e))
        return fs

    def include_files(self, include):
        """nel file host sostitusce ogni parametro
        con il file ad esso collegato

        Args:
            js (dict): "include". ramo del project
        """
        loginfo.log(os.linesep,">> include")
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
                sp = param_path.split('|')
                param = sp[0]
                path = sp[1]
                loginfo.log(f"{param}: {path}")
                with open(path, "rt") as f:
                    txt = f.read()
                host = host.replace(param, txt)
            #
            for key_val in param_lst:
                sp = key_val.split('|')
                key = sp[0]
                val = sp[1]
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
        loginfo.log(os.linesep,"*>> exe_dir")
        try:
            dr = self.get(exe_dir, 'dir')
            ptrn = self.get(exe_dir, 'ptrn')
            prog = self.get(exe_dir, 'prog')
            prog = self.list2str(prog)
            par_name = self.get(exe_dir, 'par_name')
            sub = self.get(exe_dir, 'par_sub')
            # replace par in par_name
            sp = sub.split('|')
            files = self.files_of_dir(dr, ptrn)
            for f in files:
                file_name = os.path.basename(f)
                par = file_name.replace(sp[0], sp[1])
                x = prog.replace(par_name, par)
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
        loginfo.log(os.linesep,">> remove_dir")
        try:
            for de in remove_dir:
                loginfo.log(de)
                dr = de.get('dir')
                ptrn = de.get('ptrn')
                files = self.files_of_dir(dr, ptrn)
                for f in files:
                    loginfo.log(f)
                    os.remove(f)
        except Exception as e:
            logerr.log("remove_dir")
            logerr.log(e)
            logerr.log(pp(remove_dir))
            sys.exit(1)

    def merge_files(self, merge):
        loginfo.log(os.linesep,">> merge")
        out = self.get(merge, "out")
        files = self.get(merge, "files")
        fout = open(out, "w+")
        for f in files:
            loginfo.log(f)
            with open(f, "rt") as f:
                txt = f.read()
            fout.write(txt)
        fout.close()
        loginfo.log(out)
        os.chmod(out, 0o666)

    def execute_programs(self, exe):
        loginfo.log(os.linesep,">> exe")
        # set_trace()
        for x in exe:
            x = self.list2str(x)
            loginfo.log(x)
            r = os.system(x)
            if r != 0:
                logerr.log("exe:", x)
                logerr.log(r)
                sys.exit(1)

    def parse_json(self, js):
        for k, v in js.items():
            if k == "exe":
                self.execute_programs(v)
            elif k == "merge":
                self.merge_files(v)
            elif k == "include":
                self.include_files(v)
            elif k == "exe_dir":
                self.execute_files_of_dir(v)
            elif k == "remove_dir":
                self.remove_files_of_dir(v)
            else:
                pass

    def parse(self, in_path):
        try:
            with open(in_path, "r") as f:
                txt = f.read()
            js = json.loads(txt)
        except Exception as e:
            logerr.log("json ERROR")
            logerr.log(e)
            sys.exit(1)
        self.parse_json(js)


def do_main(src_path):
    PrjMgr().parse(src_path)


def prn_es():
    js = {
        "exe": [
            [
                "teimxml.py",
                "-i prova01.txt",
                "-t tags01.csv",
                "-o prova01_v.txt"
            ],
            "teimlineword.py -i prova01_v.txt -o prova01_vlw.xml",
            "xmllint --format prova01_vlw.xml -o prova01_vlwf.xml",
            "teimdict.py -i prova01.txt -o prova01_d.csv"
        ],
        "merge": {
            "out": "floripar1.txt",
            "files": [
                "./eps/fl_par1_ep12.txt",
                "./eps/fl_par1_ep13.txt",
                "./eps/fl_par1_ep14.txt",
                "./eps/fl_par1_ep16.txt",
                "./eps/fl_par1_ep17.txt",
            ]
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
            "ptrn": ".xml",
            "par_sub": ".xml|",
            "par_name": "$F",
            "prog": [
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
                "ptrn": "pa_list*.html"
            }
        ]

    }

    loginfo.log(pp(js))


if __name__ == "__main__":
    if len(sys.argv) == 1:
        prn_es()
        sys.exit()
    do_main(sys.argv[1])
