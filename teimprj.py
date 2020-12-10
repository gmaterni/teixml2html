#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
import sys
import pprint
pp = pprint.PrettyPrinter(indent=2, width=70)


__date__ = "11-08-2020"
__version__ = "0.2.1"
__author__ = "Marta Materni"


class PrjMgr(object):

    def __init__(self):
        pass

    def prn(self, s):
        print(s)

    def execute(self, exs):
        self.prn(" ")
        for x in exs:
            self.prn(x)
            s = os.system(x)
            if s != 0:
                sys.exit()

    def exemerge(self, merge):
        self.prn(" ")
        out = merge.get("out", None)
        if out is None:
            self.prn("out error")
            sys.exit()
        files = merge.get("files", None)
        if files is None:
            self.prn("files error")
            sys.exit()
        fout = open(out, "w+")
        for f in files:
            self.prn(f)
            with open(f, "rt") as f:
                txt = f.read()
            fout.write(txt)
        fout.close()
        self.prn(" ")
        self.prn(out)
        os.chmod(out, 0o666)

    def parse(self, in_path):
        with open(in_path, "r") as f:
            txt = f.read()
        js = json.loads(txt)

        exe = js.get('exe', None)
        if exe is not None:
            self.execute(exe)

        merge = js.get('merge', None)
        if merge is not None:
            self.exemerge(merge)


def do_main(src_path):
    alwp = PrjMgr()
    alwp.parse(src_path)


def prn_es():
    s="""
teimprj.py <file.json>

es. file progetto  json

    """
    print(s)
    js = {
        "exe": [
            "teimxml.py -i prova01.txt -t tags01.csv -o prova01_v.txt",
            "teimlineword.py -i prova01_v.txt -o prova01_vlw.xml",
            "xmllint  --format prova01_vlw.xml -o prova01_vlwf.xml",
            "teimdict.py -i prova01.txt -o prova01_d.csv"
        ]
    }
    pp.pprint(js)


if __name__ == "__main__":
    args = sys.argv[1:]
    if len(args) == 0:
        prn_es()
        sys.exit()
    do_main(args[0])
