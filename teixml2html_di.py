#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pdb import set_trace
import os
import sys
import argparse
from teixml2html import Xml2Html

__date__ = "20-12-2020"
__version__ = "0.0.2"
__author__ = "Marta Materni"


def do_mauin(xml_name, html_name,confd, confi, debug_liv=0):
    """invoca teixml2html.py 
    con tagsd per la diplomatica
    produce un file hatml_named.html (aggiunge d) e hatml_named_F.html
    
    con tagsi per la interpretativa
    produce un file hatml_namei.html (aggiunge i) e hatml_nameiF.html

    unisce hatml_named.htm l e hatml_namei.html in html_name.html

    cancella html_named.html e html_namei.html


    Args:
        xml_name (str): file.xml
        html_name (str): file.html
        confd (str): file.json diplomatica
        confi (str]): file.json interpretativa
        deb (bool, optional): attivazione debug. Defaults to False.
    """
    xt = Xml2Html()
    html_name_dipl = html_name.replace(".html", "d.html")
    path_html_dipl=xt.write_html(xml_name, html_name_dipl, confd,  debug_liv)
    #
    html_name_inter = html_name.replace(".html", "i.html")
    path_html_inter=xt.write_html(xml_name, html_name_inter, confi, debug_liv)
    #
    fout = open(html_name, "w+")
    with open(path_html_dipl, "rt") as f:
        txt = f.read()
    # TODO applicazione html params
    txt=xt.set_html_pramas(txt)
    fout.write(txt)
    fout.write(os.linesep)
    #
    with open(path_html_inter, "rt") as f:
        txt = f.read()
    # TODO applicazione html params
    txt=xt.set_html_pramas(txt)
    fout.write(txt)
    fout.close()
    os.chmod(html_name, 0o666)
    os.remove(path_html_dipl)
    os.remove(path_html_inter)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    if len(sys.argv) == 1:
        print("release: %s  %s" % (__version__, __date__))
        parser.print_help()
        sys.exit()
    parser.add_argument('-d',
                        dest="deb",
                        required=False,
                        metavar="",
                        default=0,
                        help="[-d 0/1/2](setta livello di debug)")
    parser.add_argument('-cd',
                        dest="cnfd",
                        required=True,
                        metavar="",
                        help="-c <file_conf.json> (diplomatuca")
    parser.add_argument('-ci',
                        dest="cnfi",
                        required=True,
                        metavar="",
                        help="-c <file_conf.json> (interpretativa")
    parser.add_argument('-i',
                        dest="xml",
                        required=True,
                        metavar="",
                        help="-i <file_in.xml>")
    parser.add_argument('-o',
                        dest="html",
                        required=True,
                        metavar="",
                        help="-o <file_out.html>")
    args = parser.parse_args()
    do_mauin(args.xml, args.html, args.cnfd, args.cnfi, args.deb)
