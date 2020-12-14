#!/usr/bin/env python3
# -*- coding: utf-8 -*-

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


__date__ = "13-12-2020"
__version__ = "0.2.2"
__author__ = "Marta Materni"

logerr = Log()


class PrjMgr(object):

    def __init__(self):
        logerr.open("log/teimprj.err.log", 1)

    def execute(self, x):
        print(x)
        s = os.system(x)
        if s != 0:
            logerr.log("Error execute:", x)
            logerr.log(s)
            sys.exit()

    def execute_programs(self, exs):
        for x in exs:
            print(x)
            s = os.system(x)
            if s != 0:
                logerr.log("Error execute:", x)
                logerr.log(s)
                sys.exit()

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
            print(f)
            with open(f, "rt") as f:
                txt = f.read()
            fout.write(txt)
        fout.close()
        print(out)
        os.chmod(out, 0o666)

    def parse_json(self, js):
        for k, v in js.items():
            if isinstance(v, dict):
                self.parse_json(v)
                continue
            if k == "exe":
                self.execute_programs(v)
            if k in ["files","out"]:
                pass
            elif k == "merge":
                self.merge_files(v)
            else:
                if isinstance(v, str):
                    self.execute(v)
                    pass

    def parse(self, in_path):
        with open(in_path, "r") as f:
            txt = f.read()
        js = json.loads(txt)
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
        }
    }
    print(pp(js))


if __name__ == "__main__":
    args = sys.argv[1:]
    if len(args) == 0:
        prn_es()
        sys.exit()
    do_main(args[0])
