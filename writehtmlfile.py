#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import argparse
from ualog import Log

__date__ = "04-01-2021"
__version__ = "0.1.0"
__author__ = "Marta Materni"

logerr = Log("a")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    if len(sys.argv) == 1:
        print("release: %s  %s" % (__version__, __date__))
        parser.print_help()
        sys.exit()
    try:
        parser.add_argument('-i',
                            dest="inh",
                            required=True,
                            metavar="",
                            help="-i <file_in.html>")
        parser.add_argument('-o',
                            dest="ouh",
                            required=True,
                            metavar="",
                            help="-o <file_out.html>")
        parser.add_argument('-wa',
                            dest="wa",
                            required=False,
                            metavar="",
                            default="a",
                            help="[-wa w/a (w)rite a)ppend) default a")
        args = parser.parse_args()
        html_in=args.inh
        html_ou=args.ouh
        write_append=args.wa
        with open(html_in, "rt") as f:
            txt = f.read()
        with open(html_ou, write_append) as f:
            f.write(txt)
    except Exception as e:
        logerr.log("ERROR writehtmlfile.py")
        logerr.log(e)
        sys.exit(1)
