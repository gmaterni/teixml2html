#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pdb import set_trace
import os
import re
import sys
from lxml import etree
import pprint
import sys
import copy
import argparse
from readhtmlconf import read_html_conf
from readjson import read_json
from htmlbuilder import HtmlBuilder
from htmloverflow import HtmlOvweflow
from ualog import Log
from uainput import Inp

__date__ = "19-12-2020"
__version__ = "0.0.5"
__author__ = "Marta Materni"


def pp(data):
    if data is None:
        return ""
    s = pprint.pformat(data, indent=2, width=120)
    return s+os.linesep


logconf = Log("w")
loginfo = Log("a")
logerr = Log("a")
inp = Inp()

class Xml2Html(object):

    def __init__(self):
        logconf.open("log/teixml2html.cnf.log", 0)
        loginfo.open("log/teixml2html.log", 0)
        logerr.open("log/teixml2html.err.log", 1)
        self.xml_path = None
        self.html_path = None
        self.man_conf = None
        self.html_conf = None
        self.before_id = None
        self.hb = None
        self.xml_data_lst = None
        self.xml_data_dict = None
        self.is_container_stack = None
        self.csv_tag_err = None

    def node_liv(self, node):
        d = 0
        while node is not None:
            d += 1
            node = node.getparent()
        return d - 1

    def clean_key(self, k):
        s = k
        p0 = k.find("{http")
        if (p0 > -1):
            p1 = k.rfind('}')
            if p1 > -1:
                s = k[p1+1:]
        return s

    def node_items(self, nd):
        kvs = nd.items()
        js = {}
        for kv in kvs:
            k = self.clean_key(kv[0])
            v = kv[1]
            js[k] = v
        return js

    def node_tag(self, nd):
        tag = nd.tag
        tag = tag if type(nd.tag) is str else "XXX"
        p = tag.rfind('}')
        if p > 1:
            logerr.log("ERROR in  xml")
            logerr.log(nd.tag)
            sys.exyt()
        return tag.strip()

    def node_id(self, nd):
        s = ''
        kvs = nd.items()
        for kv in kvs:
            if kv[0].rfind('id') > -1:
                s = kv[1]
                break
        return s

    def node_id_num(self, id):
        if id == '':
            return ""
        m = re.search('\d', id)
        if m is None:
            return -1
        p = m.start()
        return id[p:]

    def node_text(self, nd):
        text = nd.text
        text = '' if text is None else text.strip()
        text = text.strip().replace(os.linesep, ',,')
        return text

    def node_tail(self, nd):
        tail = '' if nd.tail is None else nd.tail
        tail = tail.strip().replace(os.linesep, '')
        return tail

    def node_val(self, nd):
        ls = []
        for x in nd.itertext():
            s = x.strip().replace(os.linesep, '')
            ls.append(s)
        texts = ' '.join(ls)
        s = re.sub(r"\s{2,}", ' ', texts)
        return s

    def node_is_parent(self, nd):
        cs = nd.getchildren()
        l = len(cs)
        return l > 0

    def get_node_data(self, nd):
        items = self.node_items(nd)
        id = self.node_id(nd)
        if id != '':
            id_num = self.node_id_num(id)
            items['id_num'] = id_num
        return {
            'id': id,
            'liv': self.node_liv(nd),
            'tag': self.node_tag(nd).lower(),
            'tail': self.node_tail(nd),
            'text': self.node_text(nd),
            'items': items,
            # 'keys': self.node_keys(nd),
            # 'val':self.node_val(nd),
            'is_parent': self.node_is_parent(nd)
        }

    def text_format(self, text, pars):
        """ formatta text utilizzado attrs
            pqrw={'k0':'val0','k1':'val1', ..}

        Args:
            text (str): testo
            pars ( dict): [parametri

        Returns:
            str : testo formattato
        """
        try:
            ms = re.findall("[%]\w+[%]", text)
            ks = [x.replace('%', '') for x in ms]
            for k in ks:
                v = pars.get(k, f'%{k}%')
                text = text.replace(f'%{k}%', v)
            return text
        except Exception as e:
            logerr.set_out(1)
            logerr.log(os.linesep, "Error", "text_format()")
            logerr.log(e)
            logerr.log(f"text:{text}")
            logerr.log(f"pars: {pars}")
            sys.exit()

    def attrs_format(self, text, pars):
        """formatta html_attr_str se il parametro
            non esiste lo rimuove
            aggiusta gli argommenti di class

        Args:
            text (str): testo
            pars (list): patametri

        Returns:
            str: testo con i parametri settai
        """
        ms = re.findall("[%]\w+[%]", text)
        ks = [x.replace('%', '') for x in ms]
        for k in ks:
            v = pars.get(k, '')
            text = text.replace(f'%{k}%', v)
        return text

    def class_adjust(self, text):
        text = text.replace(' "', '"')
        text = text.replace(' _int', '')
        p0 = text.find('class')
        if p0 > -1:
            p1 = text.find('"', p0+5)
            p2 = text.find('"', p1+1)
            s0 = text[:p2]
            s1 = text[p2:]
            text = s0.replace('#', '')+s1
        return text

    def items_extend(self, x_data, csv_data,):
        """unisce  x_data.items e csv_data.attrs
        se in csv é settato parent aggiunge gli x_iitems del paremt

        Args:
            x_data (dict): data estratto da xml
            csv_data (dict): data estartto dat fiele html..:csv

        Returns:
            dicct: unione dei due dict
        """
        attrs = {}
        # TODO parent x_data items
        csv_tag_parent = csv_data.get('parent', None)
        if csv_tag_parent is not None:
            x_data_parent = self.xml_data_dict.get(csv_tag_parent, None)
            if x_data_parent is not None:
                items = x_data_parent.get('items', {})
                attrs = copy.deepcopy(items)
        # x_data items
        items = x_data.get('items', {})
        for k, v in items.items():
            attrs[k] = v
        # csv_data attrs
        c_attrs = csv_data.get('attrs', {})
        for k, v in c_attrs.items():
            attrs[k] = v
        return attrs

    def attrs_builder(self, x_items, c_keys=[], c_attrs={}):
        """seleziona gli elemnti di x_items filtrati da c_kets
             aggiunge gli elementi c_attrs {}

        Args:
            x_items ([dict]): xml items
            c_keys (dict, optional): keys seleziona fi element di x_items 
            c_attrs (dict, optional): csv attr

        Returns:
            attrs (dict): dict unione dei parametri e degli items del parent
        """
        attrs = {}
        try:
            # set_trace()
            for k in c_keys:
                attrs[k] = x_items[k]
            for k in c_attrs.keys():
                attrs[k] = c_attrs[k]
        except Exception as e:
            logerr.log(os.linesep, "ERROR: attrs_builder()")
            logerr.log(e)
            logerr.log("x_items:", x_items)
            logerr.log("c_keys: ", c_keys)
            logerr.log("c_attrs:", c_attrs)
            sys.exit()
        return attrs

    def attrs2html(self, attrs):
        """trasforma in tag htnl il attrs di html
            ordina partendo da class, id s esistono

        Args:
            attrs (dict): attrs di html

        Returns:
            str: attrs htnl
        """
        ks = []
        if 'class' in attrs.keys():
            ks.append('class')
        if 'id' in attrs.keys():
            ks.append('id')
        for k in attrs.keys():
            if k not in ['id', 'class']:
                ks.append(k)
        ls = []
        for k in ks:
            v = attrs[k]
            if k == 'id':
                v = f'{self.before_id}{v}'
            s = f'{k}="{v}"'
            ls.append(s)
        return " ".join(ls)

    def get_row_conf_data(self, x_data):
        """ ritorna dati della row di <tag>.csvindividuata
            dall tag o tag+attr di x_data del file xml
            memorizza x_data  in xml_data_dict
            la key è quella ottenuta dal tag xml e l'eventuale/i attributo

        Args:
            x_data (dict):xml data

        Returns:
            [row_data (dict): dati estartti da csv
        """
        xml_tag = x_data['tag']
        row_data = self.html_conf.get(xml_tag, None)
        if row_data is None:
            row_data = self.html_conf.get('x', {})
            csv_tag = xml_tag
            self.csv_tag_err = f'_x_{csv_tag}'
        else:
            tag = row_data.get('tag', f"_x_{xml_tag}")
            p = tag.find('+')
            if p > -1:
                x_items = x_data['items']
                # tag|tag + att1_name + attr2_name+..
                # x_items[attr<n>_name]  => [attr1_val,attr2_val]
                # #tag + attr1_val + att2_vap + ..
                lsk = tag.split('+')[1:]
                lsv = [x_items[k] for k in lsk if k in x_items.keys()]
                attrs_val = '+'.join(lsv)
                csv_tag = xml_tag+'+'+attrs_val
                row_data = self.html_conf.get(csv_tag, None)
                if row_data is None:
                    row_data = self.html_conf.get('x+y', None)
                    self.csv_tag_err = f'_xy_{csv_tag}'
                else:
                    self.csv_tag_err = csv_tag
            else:
                csv_tag = xml_tag
                self.csv_tag_err = csv_tag
        self.xml_data_dict[csv_tag] = x_data
        return row_data

    def build_content(self, tag, attrs, text, tail):
        t = f'<{tag} {attrs}>{text}</{tag}>{tail}'
        return t

    def build_html_tag(self, x_data):
        """raccogli i dati per costruire un elemnt html

        Args:
            x_data (dict): dati presi da xml

        Returns:
            dict: dati necessari a costruire html
        """
        x_items = x_data['items']
        x_text = x_data['text']
        x_liv = x_data['liv']
        self.is_container_stack[x_liv] = False
        c_data = self. get_row_conf_data(x_data)
        ################################
        if inp.prn:
            loginfo.log("============").prn()
            loginfo.log(">> x_data").prn()
            loginfo.log(pp(x_data)).prn()
            loginfo.log(">> csv_data").prn()
            loginfo.log(pp(c_data)).prn()
        ################################
        c_tag = c_data.get('tag')
        # c_keys sone le key degli elementi di items da prendere
        c_keys = c_data.get('keys', [])
        c_attrs = c_data.get('attrs', {})
        c_text = c_data.get('text', "")
        c_params = c_data.get('params', {})
        html_attrs = self.attrs_builder(x_items, c_keys, c_attrs)
        html_attrs_str = self.attrs2html(html_attrs)
        ext_items = self.items_extend(x_data, c_data)
        # formatta attr utilizzando x_items
        if html_attrs_str.find('%') > -1:
            html_attrs_str = self.attrs_format(html_attrs_str, x_items)
            html_attrs_str = self.class_adjust(html_attrs_str)
        # formatta c_text itilizzando ext_items :items + parent.items)
        if c_text.find('%') > -1:
            c_text = self.text_format(c_text, ext_items)
            # formatta c_text utilizzando %text% se esiste lo elimina
            if c_text.find('%text%') > -1:
                if x_data.get('is_parent', None) is False:
                    c_text = c_text.replace('%text%', x_text)
                    x_text = ''
                else:
                    self.is_container_stack[x_liv] = True
            # ormatta c_text utilizzando c_params
            if c_text.find('%') > -1:
                c_text = self.text_format(c_text, c_params)
        #
        html_text = x_text+c_text
        # errori nella gestione del files csv dei tag html
        if self.csv_tag_err.find('_x') > -1:
            logerr.log("ERRORO in csv").prn()
            logerr.log("xml:",pp(x_data))
            s = f'csv: {self.csv_tag_err}'
            logerr.log(s,os.linesep).prn()
            inp.inp("!")
        ####################
        html_data = {
            'tag': c_tag,
            'attrs': html_attrs_str,
            'text': html_text
        }
        ################################
        if inp.prn:
            loginfo.log(">> htl_data").prn()
            loginfo.log(pp(html_data)).prn()
            loginfo.log(">> ext_items").prn()
            loginfo.log(pp(ext_items)).prn()
        ################################
        return html_data

    def html_append(self, nd):
        x_data = self.get_node_data(nd)
        self.xml_data_lst.append(x_data)
        x_tag = x_data['tag']
        x_liv = x_data['liv']
        x_is_parent = x_data['is_parent']
        x_tail = x_data['tail']
        h_data = self.build_html_tag(x_data)
        h_tag = h_data['tag']
        h_text = h_data['text']
        h_attrs = h_data['attrs']
        # TODO se il precedente è un parent contenitor
        is_container = self.is_container_stack[x_liv-1]
        if is_container:
            content = self.build_content(h_tag, h_attrs, h_text, x_tail)
            s = self.hb.tag_last()
            content = s.replace('%text%', content)
            self.hb.upd_tag_last(content)
            h_tag = 'XXX'
        if x_is_parent:
            self.hb.opn(x_liv, h_tag, h_attrs, h_text, x_tail)
        else:
            self.hb.ovc(x_liv, h_tag, h_attrs, h_text, x_tail)
        ################################
        if inp.prn:
            loginfo.log(">> html node").prn()
            loginfo.log(self.hb.tag_last()).prn()
        inp.inp(x_tag)
        if inp.equals('?'):
            print(self.hb.html_format())
            inp.inp()
        ################################

    def set_html_pramas(self, html):
        """utilizzando il file json formatta i parametri residui
            es. il nome del manoscrittp %MAN%
            qualsiasi altro parametro definito nel file cid configurazione
            al tag html_params

        Args:
            html (str): html 

        Returns:
            html (str): html con settati i parametri         """
        pars = self.man_conf.get("html_params", {})
        for k, v in pars.items():
            html = html.replace(k, v)
        return html

    def write_html(self, xml_path, html_path, csv_path, json_path, deb=False):
        """fa il parse del file xml_path scrive i files:
            nel formato comapatto: <html_path>
            formato indentato <html_name>_f.html

        Args:
            xml_path (str]:  file xml
            html_path (str): file html
            csv_path (str): file dei tags di elaborazione
            json_path (str): file di configurazoine
            deb (bool, optional): flag per gestione debuf

        Returns:
            html_path (str): filr name html 
        """
        inp.enable(deb)
        self.xml_data_lst=[]
        self.xml_path = xml_path
        self.html_path = html_path
        # lettura configurazioni
        self.man_conf = read_json(json_path)
        logconf.log(">> man_coonf", pp(self.man_conf)).prn(0)
        self.html_conf = read_html_conf(csv_path)
        logconf.log(">> html_conf", pp(self.html_conf)).prn(0)
        # TODO prefisso di  id per diplomatia e interpretativa
        rd = self.html_conf.get("before_id", {})
        self.before_id = rd.get('tag', "")
        self.hb = HtmlBuilder()
        self.xml_data_dict = {}
        self.is_container_stack = [False for i in range(1, 20)]
        # tag per controlo errori
        self.csv_tag_err = ""
        #
        self.hb.init()
        try:
            xml_root = etree.parse(self.xml_path)
        except Exception as e:
            logerr.log(e)
            sys.exit()
        for nd in xml_root.iter():
            self.html_append(nd)
        self.hb.del_tags('XXX')
        self.hb.end()
        #############################
        """gestisce il settaggio degli overflow
        modifica il parametro html_lst

        Returns:
            [type]: [description]
        """        
        html_lst=self.hb.get_tag_lst()
        html_over=HtmlOvweflow(self.xml_data_lst,html_lst,self.html_conf)
        html_over.set_overflow()
        ############################
        # html su una riga versione per produzione
        html = self.hb.html_onerow()
        html = self.set_html_pramas(html)
        with open(self.html_path, "w+") as f:
            f.write(html)
        os.chmod(self.html_path, 0o666)
        #
        # html formattato versione per il debug
        # file_name.html => file_name_X.html
        html = self.hb.html_format()
        html = self.set_html_pramas(html)
        path = self.html_path.replace(".html", "_F.html")
        with open(path, "w+") as f:
            f.write(html)
        os.chmod(self.html_path, 0o666)
        return self.html_path


def do_mauin(xml, html, tags, conf, deb=False):
    Xml2Html().write_html(xml, html, tags, conf, deb)


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
                        dest="tag",
                        required=True,
                        default="",
                        metavar="",
                        help="-t <file_hml_tags.csv>")
    parser.add_argument('-c',
                        dest="cnf",
                        required=True,
                        metavar="",
                        help="-c <file_conf.json")
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
    if args.html == args.xml:
        print("Name File output errato")
        sys.exit(0)
    do_mauin(args.xml, args.html, args.tag, args.cnf, args.deb)
