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


def do_mauin(xml_name, html_name, confd, confi, templ_name, deb=False):
    """invoca teixml2html.py 
    con tagsd per la diplomatica
    produce un file hatml_named.html (aggiunge d) e hatml_named_F.html

    con tagsi per la interpretativa
    produce un file hatml_namei.html (aggiunge i) e hatml_nameiF.html

    unisce hatml_named.htm l e hatml_namei.html in html_name.html

    cancella html_named.html e html_namei.html
template:

<div id="MAN_dip_id" class="text_pannel tei_dip">
    INCLUDE
</div>
<div id="MAN_int_id" class="text_pannel tei_int">
    INCLUDE
</div>

    Args:
        xml_name (str): file.xml
        html_name (str): file.html
        confd (str): file.json diplomatica
        confi (str]): file.json interpretativa
        trmpl_name (str]): file template
        deb (bool, optional): attivazione debug. Defaults to False.
    """
    try:
        with open(templ_name, "rt") as f:
            templ = f.read()
        templ_lst=templ.split('INCLUDE')
        #
        xt = Xml2Html()
        html_name_dipl = html_name.replace(".html", "d.html")
        html_path_dipl = xt.write_html(xml_name, html_name_dipl, confd,  deb)
        #
        html_name_inter = html_name.replace(".html", "i.html")
        html_path_inter = xt.write_html(xml_name, html_name_inter, confi, deb)
        #
        with open(html_path_dipl, "rt") as f:
            txt = f.read()
            hd=f'{templ_lst[0]}{txt}{templ_lst[1]}'
        with open(html_path_inter, "rt") as f:
            txt = f.read()
            hi=f'{txt}{templ_lst[2]}'
        hdi=hd+hi
        with open(html_name, "w+") as f:
            f.write(hdi)
        #
        os.chmod(html_name, 0o666)
        os.remove(html_path_dipl)
        os.remove(html_path_inter)
    except Exception as e:
        print(e)
        sys.exit(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    if len(sys.argv) == 1:
        print("release: %s  %s" % (__version__, __date__))
        parser.print_help()
        sys.exit()
    parser.add_argument('-d',
                        dest="deb",
                        required=False,
                        action="store_true",
                        default=False,
                        help="[-d ](abilita debug)")
    parser.add_argument('-t',
                        dest="templ",
                        required=True,
                        metavar="",
                        help="-t file template html>")
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
    do_mauin(args.xml, args.html, args.cnfd, args.cnfi,args.templ, args.deb)
