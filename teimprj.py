#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pdb import set_trace
import os
import json
import sys
import pprint
from ualog import Log


def pp(data):
    if data is None:
        return ""
    s = pprint.pformat(data, indent=2, width=120)
    return s+os.linesep


__date__ = "20-12-2020"
__version__ = "0.3.1"
__author__ = "Marta Materni"

logerr = Log("a")
loginfo = Log("a")


class PrjMgr(object):

    def __init__(self):
        logerr.open("log/teimprj.err.log", 1)
        loginfo.open("log/teimprj.log", 1)

    def include_files(self, js):
        """nel file host sostitusce ogni parametro
        con il file ad esso collegato

        Args:
            js ([type]): [description]
        """
        file_host = js.get("host", None)
        file_dest = js.get("dest", None)
        par_path_list = js.get("files")
        with open(file_host, "rt") as f:
            host = f.read()
        #
        for par_path in par_path_list:
            sp = par_path.split('|')
            param = sp[0]
            path = sp[1]
            loginfo.log(param)
            loginfo.log(path)
            with open(path, "rt") as f:
                txt = f.read()
            host = host.replace(param, txt)
        #
        with open(file_dest, "w+") as f:
            f.write(host)
        os.chmod(file_dest, 0o666)

    def files_of_dir(self, dr, ext):
        files = []
        try:
            for f in os.listdir(dr):
                fpath = os.path.join(dr, f)
                if os.path.isfile(fpath) is False:
                    continue
                if ext != "":
                    name = os.path.basename(fpath)
                    if name.find(ext) < 0:
                        continue
                files.append(fpath)
        except Exception as e:
            logerr.log(e)
            logerr.log(f'dir:{dr}  ext:{ext}')
            sys.exit(1)
        return files

    def execute_files_of_dir(self,js):
        
        try:
            def get(k):
                s=js.get(k,None)
                if s is None:
                    raise Exception(f"{k} not found.{os.linesep}")
                return s
            
            dr=get('dir')
            ext=get('ext')
            prog=get('prog')
            par_name=get('par_name')
            sub=get('par_sub')
            sp=sub.split('|')        
            files = self.files_of_dir(dr, ext)
            for f in files:
                file_name=os.path.basename(f)
                par=file_name.replace(sp[0],sp[1])
                x=prog.replace(par_name,par)
                loginfo.log(x)
                r=os.system(x)
                if r!=0:
                    logerr.log("ERROR execute:", x)
                    logerr.log(s)
                    sys.exit()

        except Exception as e:
            logerr.log(e)
            logerr.log(str(js))
            logerr.log(pp(js))
            sys.exit(0)

    def merge_files(self, merge):
        out = merge.get("out", None)
        if out is None:
            logerr.log("tag merrge out is null")
            sys.exit()
        files = merge.get("files", None)
        if files is None:
            logerr.log("tag files is null")
            sys.exit()
        fout = open(out, "w+")
        for f in files:
            loginfo.log(f)
            with open(f, "rt") as f:
                txt = f.read()
            fout.write(txt)
        fout.close()
        loginfo.log(out)
        os.chmod(out, 0o666)

    def execute_program(self, x):
        loginfo.log(x)
        s = os.system(x)
        if s != 0:
            logerr.log("ERROR execute:", x)
            logerr.log(s)
            sys.exit()

    def execute_programs(self, exs):
        for x in exs:
            loginfo.log(x)
            s = os.system(x)
            if s != 0:
                logerr.log("ERROR execute:", x)
                logerr.log(s)
                sys.exit()

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
            elif k in ["files", "out", "host", "dest"]:
                pass
            else:
                if isinstance(v, str):
                    self.execute_program(v)

    def parse(self, in_path):
        try:
            with open(in_path, "r") as f:
                txt = f.read()
            js = json.loads(txt)
        except Exception as e:
            logerr.log("json ERROR")
            logerr.log(e)
            sys.exit()
        self.parse_json(js)


def do_main(src_path):
    PrjMgr().parse(src_path)


def prn_es():
    js = {
        "exe": [
            "teimxml.py -i prova01.txt -t tags01.csv -o prova01_v.txt",
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
            "files": [
                "EPISODE_LIST_DIPL|html/par/txt/par_listd.html",
                "EPISODE_LIST_INTER|html/par/txt/par_listi.html"
            ]
        }
    }
    loginfo.log(pp(js))


if __name__ == "__main__":
    if len(sys.argv) == 1:
        prn_es()
        sys.exit()
    do_main(sys.argv[1])
