#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pdb import set_trace
from lxml import etree
import os
import argparse
import sys
import pprint
from ualog import Log
from xml_const import *
import re


__date__ = "15-01-2021"
__version__ = "0.2.0"
__author__ = "Marta Materni"


logerr = Log("w")
loginfo = Log("w")


def pp_data(data):
    s = pprint.pformat(data, indent=0, width=80)
    return s


"""
splitta path_xml_in negli episodi ci scribe in dir_out
produce <man>_list.xml con l'elenco degli episodi e scrive in dir_out
produce <man>_list.txt con l'elenco degli episodi e scrice i dir_out
"""


class XmlSplitEps:

    def __init__(self, path_xml_in, dir_out, sigla_man):
        self.path_xml_in = path_xml_in
        self.dir_out = dir_out
        self.sigla_man = sigla_man
        # path_err = dir_out + "_eps_ERR_.log"
        path_err = os.path.join(dir_out, "split_ERR.log")
        logerr.open(path_err, out=1)
        path_info = os.path.join(dir_out, "spli.log")
        loginfo.open(path_info, out=0)
        self.body = None
        self.back = None

    def set_body_back(self):
        try:
            root = etree.parse(self.path_xml_in)
            xml = etree.tostring(root,
                                method='xml',
                                xml_declaration=None,
                                encoding='unicode',
                                with_tail=True,
                                pretty_print=False,
                                strip_text=False
                                )
            m = re.search(BODY_TOP_PATTERN, xml)
            p0 = m.start()
            m = re.search(BODY_BOTTOM_PATTERN, xml)
            p1 = m.end()
            xml_body = xml[p0:p1]
            loginfo.log(xml_body)
            self.body = etree.fromstring(xml_body)
            #
            m = re.search(BACK_TOP, xml)
            if m is None:
                return
            p0 = m.start()
            m = re.search(BACK_BOTTOM, xml)
            p1 = m.end()
            xml_back = xml[p0:p1]
            loginfo.log(xml_back)
            self.back = etree.fromstring(xml_back)
        except Exception as e:
            logerr.log("splitteixml.py set_body_back()")
            logerr.log(str(e))
            sys.exit(1)

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
        except Exception as e:
            logerr.log("splitteixml.py write_eps_xml()")
            s = str(e)
            logerr.log(s)
            sys.exit(1)

    # write xml/par/par.xml
    def writ_eps_xml_lst(self, eps_lst, xml_path):
        xml_src = os.linesep.join(eps_lst)
        with open(xml_path, "w+") as fw:
            fw.write(xml_src)
        os.chmod(xml_path, 0o666)

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

    def build_episode_name(self, eps):
        f = self.dir_out
        dir = os.path.dirname(f)
        # name = eps
        path = os.path.join(dir, eps)
        return path

    def build_list_name(self, ext):
        name = self.sigla_man + "_list" + ext
        path = os.path.join(self.dir_out, name)
        return path

    def get_notes(self):
        # TODO get_root
        if self.back is None:
            return ""
        root_back = self.back
        note=root_back.find('div')
        nds = note.findall('teimed_note')
        ls = []
        for nd in nds:
            xml_node = etree.tostring(nd,
                                      method='xml',
                                      xml_declaration=None,
                                      encoding='unicode',
                                      with_tail=True,
                                      pretty_print=True)
            ls.append(xml_node.strip())
        s = "".join(ls)
        return s

    def node_tag(self, nd):
        tag = nd.tag if type(nd.tag) is str else "XXX_no_tag"
        pid = tag.find('}')
        if pid > 0:
            tag = tag[pid + 1:]
        return tag.strip()

    def prn_node(self, nd):
        # TODO stampa nodo nel log
        return
        tag = self.node_tag(nd)
        ks = self.node_attrs(nd)
        s = pp_data(ks)
        loginfo.log(tag + "  " + s)

    def get_child(self, nd, tag=None):
        child = None
        for d in nd.iterchildren(tag=None):
            child = d
            break
        return child

    """
    trova episodio corrente
    controlla che inizi con pb
    trova episodio precedente
    trova ultima pagina episodio precedente
    inserisce la pagina trova all'inzio dell'eoisodio corrente
    """

    def get_prev_pb_cb(self, nd):

        def build_node(nd):
            tag = self.node_tag(nd)
            attrs = self.node_attrs(nd)
            id = attrs.get('id', '')
            n = attrs.get('n', '')
            id = id + 'b'
            s = f'<{tag} xml:id="{id}" n="{n}" />'
            nd = etree.XML(s)
            return nd

        try:
            ep_prev = nd.getprevious()
            pb = None
            for d in ep_prev.iterdescendants(tag="pb"):
                pb = d
            if pb is None:
                raise Exception("get_prev_pb_cb() pb Not Found")
            pb = build_node(pb)
            cb = None
            for d in ep_prev.iterdescendants(tag="cb"):
                cb = d
            if cb is None:
                raise Exception("get_prev_pb_cb() cb Not Found")
            cb = build_node(cb)
        except Exception as e:
            logerr.log("splixml.py get_prev_pb_cb.")
            logerr.log("pb not found.")
            logerr.log(str(e))
            sys.exit(1)
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
        # se è la prima pagina ritona None
        if (pb):
            return None
        pb_cb = self.get_prev_pb_cb(nd)
        return pb_cb

    def write_episode_lst(self):
        self.set_body_back()
        root_body = self.body
        ls = root_body.findall('div')
        eps_lst = []
        eps_num_lst = []
        # div null per contenere la lista episodi
        eps_lst.append(NULL_TAG_START)
        for xml_node in ls:
            ks = self.node_attrs(xml_node)
            src = self.node_src(xml_node)
            # pagina iniziale con lista episoid
            eps_lst.append(src)
            # file testo con lista episodi
            eps_num = ks['ref'].replace('#', '')
            eps_num_lst.append(eps_num)
            # sottoalberi episodi
            # controllo inizio pagina
            pbcb = self.begin_pag_dupl(xml_node)
            if pbcb is not None:
                # non è la prima pagina
                pb = pbcb[0]
                cb = pbcb[1]
                self.prn_node(pb)
                self.prn_node(cb)
                ch = self.get_child(xml_node, 'lg')
                self.prn_node(ch)
                ch.addprevious(pb)
                ch.addprevious(cb)
            xml_eps_path = self.build_episode_name(eps_num + '.xml')
            self.write_eps_xml(xml_node, xml_eps_path)
        s = self.get_notes()
        loginfo.log(s)
        eps_lst.append(s)
        # chiusura div null contenitore
        eps_lst.append(NULL_TAG_END)
        # lista eps<n> in file xml
        xml_list_path = self.build_list_name(".xml")
        self.writ_eps_xml_lst(eps_lst, xml_list_path)


def do_main(path_in, dir_out, sigla_man):
    xmlspl = XmlSplitEps(path_in, dir_out, sigla_man)
    xmlspl.write_episode_lst()


if __name__ == "__main__":
    """
    es.
    dir input: xml/par/file.xml
    dir out  : xml/par/par/
    sigla_man: par
    """
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
