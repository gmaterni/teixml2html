#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from lxml import etree
import os
import argparse
import sys
import pprint
from ualog import Log
from pdb import set_trace

__date__ = "12-12-2020"
__version__ = "0.0.3"
__author__ = "Marta Materni"


logerr = Log("a")


def pp_data(data):
    s = pprint.pformat(data, indent=0, width=80)
    return s


"""
splitta path_xml_in negli episodi ci scribe in dir_out
produce <man>.xml con l'elenco degli episodi e scrive in dir_out
produce <man>.tzt con l'elenco degli episodi e scrice i dir_out 
"""


class XmlSplitEps(object):

    def __init__(self, path_xml_in, dir_out, sigla_man):
        self.path_xml_in = path_xml_in
        self.dir_out = dir_out
        self.sigla_man = sigla_man
        path_err = dir_out + "_eps_err_.log"
        logerr.open(path_err, out=1)

    # write xml/par/eps<n>
    def write_eps_xml(self, nd, name_ou):
        try:
            src = etree.tostring(nd,
                                 method='xml',
                                 xml_declaration=None,
                                 encoding='unicode',
                                 with_tail=True,
                                 pretty_print=True)
            with open(name_ou, "w+") as fw:
                fw.write(src)
            os.chmod(name_ou, 0o666)
        except etree.Error as e:
            s = str(e)
            logerr.log(s)
            # print(s)

    # write xml/par/par.xml
    def writ_eps_xml_lst(self, eps_lst, xml_path):
        xml_src = os.linesep.join(eps_lst)
        with open(xml_path, "w+") as fw:
            fw.write(xml_src)
        os.chmod(xml_path, 0o666)
        # print("xml_path",xml_path)

    # write xml/par/par.txt
    def writ_eps_num_lst(self, eps_lst, txt_path):
        txt = os.linesep.join(eps_lst)
        with open(txt_path, "w+") as fw:
            fw.write(txt)
        os.chmod(txt_path, 0o666)
        # print("eps_lst",txt_path)

    # <div type="episode" ref="#ep1">
    def node_src(self, nd):
        tag = nd.tag
        ks = self.node_attrs(nd)
        s = "<" + tag
        for k in ks:
            v = ks[k]
            s = s + ' %s="%s"' % (k, v)
        s = s + " />"
        return s

    def node_attrs(self, nd):
        attrs = {}
        if nd.attrib is None:
            return attrs
        for k, v in nd.attrib.iteritems():
            px = k.find('}')
            if px > -1:
                k = k[px + 1:]
            attrs[k] = v
        return attrs

    def eps_name(self, eps):
        f = self.dir_out
        dir = os.path.dirname(f)
        name = eps
        path = os.path.join(dir, name)
        return path

    def fl_name(self, ext):
        name = self.sigla_man + ext
        path = os.path.join(self.dir_out, name)
        return path

    def get_notes(self):
        root = etree.parse(self.path_xml_in)
        nds = root.findall('teimed_note')
        ls = []
        for nd in nds:
            src = etree.tostring(nd,
                                 method='xml',
                                 xml_declaration=None,
                                 encoding='unicode',
                                 with_tail=True,
                                 pretty_print=True)
            ls.append(src.strip())
        s = "".join(ls)
        return s

    def node_tag(self, nd):
        tag = nd.tag if type(nd.tag) is str else "XXX_no_tag"
        pid = tag.find('}')
        if pid > 0:
            tag = tag[pid + 1:]
        return tag.strip()

    def prn_node(self, nd):
        tag = self.node_tag(nd)
        ks = self.node_attrs(nd)
        s = pp_data(ks)
        # print(tag + "  " + s)

    def get_child(self, nd, tag=None):
        child = None
        for d in nd.iterchildren(tag=None):
            child = d
            break
        return child

    # trova episodio corrente
    # controlla che inizi con pb
    # trova episodio precedente
    # trova ultima pagina episodio precedente
    # inserisce la pagina trova all'inzio dell'eoisodio corrente
    def get_prev_pb_cb(self, nd):

        def build_node(nd):
            tag = self.node_tag(nd)
            attrs = self.node_attrs(nd)
            id = attrs.get('id', '')
            n = attrs.get('n', '')
            id = id + 'b'
            # n = n + 'b'
            s = '<%s xml:id="%s" n="%s" />' % (tag, id, n)
            nd = etree.XML(s)
            return nd
        try:
            ep_prev = nd.getprevious()
            for d in ep_prev.iterdescendants(tag="pb"):
                pb = d
            pb = build_node(pb)

            for d in ep_prev.iterdescendants(tag="cb"):
                cb = d
            cb = build_node(cb)
        except Exception:
            logerr.log("get_prev_pb_cb.")
            logerr.log("pb not found.")
            sys.exit()
        return [pb, cb]

    def begin_pag_dupl(self, nd):

        def find_begin_pag(nd):
            rt = True
            for d in nd.iterchildren(tag=None):
                tag = self.node_tag(d)
                if tag != 'pb':
                    rt = False
                break
            return rt
        pb = find_begin_pag(nd)
        if (pb):
            return None
        pb_cb = self.get_prev_pb_cb(nd)
        return pb_cb

    def split_eps(self):
        root = etree.parse(self.path_xml_in)
        # root.attrib["{http://www.w3.org/XML/1998/namespace}id"] = xml_id
        ls = root.findall('div')
        eps_lst = []
        eps_num_lst = []
        eps_lst.append('<TEI>')
        for nd in ls:
            ks = self.node_attrs(nd)
            src = self.node_src(nd)
            # print(src)
            # pagina iniziale con lista episoid
            eps_lst.append(src)
            # file testo con lista episodi
            eps_num = ks['ref'].replace('#', '')
            eps_num_lst.append(eps_num)
            # print(eps_num)
            # sottoalberi episodi
            # controllo inizio pagina
            pbcb = self.begin_pag_dupl(nd)
            # print(pbcb)
            if pbcb is not None:
                pb = pbcb[0]
                cb = pbcb[1]
                self.prn_node(pb)
                self.prn_node(cb)
                ch = self.get_child(nd, 'lg')
                self.prn_node(ch)
                ch.addprevious(pb)
                ch.addprevious(cb)

            xml_path = self.eps_name(eps_num + '.xml')
            self.write_eps_xml(nd, xml_path)

        s = self.get_notes()
        eps_lst.append(s)
        eps_lst.append('</TEI>')

        # lista eps<n> in file xml
        # xml/par/<mano>.xml
        xml_path = self.fl_name(".xml")
        self.writ_eps_xml_lst(eps_lst, xml_path)

        # lista eps<n> in file txt
        # xml/par/<mano>.TXT
        txt_path = self.fl_name(".txt")
        self.writ_eps_num_lst(eps_num_lst, txt_path)


def do_main(path_in, dir_out, sigla_man):
    xmlspl = XmlSplitEps(path_in, dir_out, sigla_man)
    xmlspl.split_eps()


"""
es.
dir input: xml/par/file.xml
dir out  : xml/par/par/
sigla_man: par
"""

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    if len(sys.argv) == 1:
        print("release: %s  %s" % (__version__, __date__))
        parser.print_help()
        sys.exit()
    parser.add_argument(
        '-i',
        dest="src",
        required=True,
        metavar="",
        help="-i <file.xml input>")
    parser.add_argument(
        '-o',
        dest="ou",
        required=True,
        metavar="",
        help="-o <dir out/<sigla>/")
    parser.add_argument(
        '-m',
        dest="man",
        required=True,
        metavar="",
        help="-m <sigla_maoscritto>")
    args = parser.parse_args()
    do_main(args.src, args.ou, args.man)
