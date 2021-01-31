#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import os
import pprint
import re
import sys
from pdb import set_trace

from lxml import etree

from htmlbuilder import HtmlBuilder
from htmloverflow import HtmlOvweflow
from readhtmlconf import read_html_conf
from readjson import read_json
from uainput import Inp
from ualog import Log

__date__ = "30-01-2021"
__version__ = "0.3.2"
__author__ = "Marta Materni"


def pp(data):
    if data is None:
        return ""
    s = pprint.pformat(data, indent=2, width=120)
    return s+os.linesep


logconf = Log("w")
loginfo = Log("a")
logerr = Log("a")
logcsverr = Log('a')
loghtmlerr = Log('a')
logdeb = Log('a')
inp = Inp()

class Xml2Html:

    def __init__(self):
        logconf.open("log/cfg.json", 0)
        loginfo.open("log/teixml2html.log", 0)
        logerr.open("log/teixml2html.ERR.log", 1)
        logcsverr.open("log/csv.ERR.log", 1)
        loghtmlerr.open("log/html.ERR.log", 1)
        logdeb.open("log/DEBUG.log", 0)
        self.xml_path = None
        self.html_path = None
        self.html_cfg = None
        self.html_tag_cfg = None
        # diplomatica / interpretatova (d/i)
        self.dipl_inter = None
        # prefisso di id per diplomarica / interpretativa
        self.before_id = None
        # HtmlBuilder
        self.hb = None
        # lista x_data (dati xml)
        self.xml_data_lst = None
        # dizionario di x_data (dati xml)
        self.xml_data_dict = None
        # stack dei valori v/f dei container
        self.is_container_stack = None
        # tag di controllo per erroi csv _x_ _xy_
        self.csv_tag_ctrl = None
        #flag attivo dopo un .,?,!
        self.pc_active = False
        self.w_liv=0
        # flag per gestione set_trace()
        self.trace = False

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
            sys.exyt(1)
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
            return ''
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
        le = len(cs)
        return le > 0

    def get_node_data(self, nd):
        items = self.node_items(nd)
        id = self.node_id(nd)
        if id != '':
            id_num = self.node_id_num(id)
            items['id_num'] = id_num
        return {
            'id': id,
            'liv': self.node_liv(nd),
            'tag': self.node_tag(nd),
            'text': self.node_text(nd),
            'tail': self.node_tail(nd),
            'items': items,
            # 'keys': self.node_keys(nd),
            # 'val': self.node_val(nd),
            'is_parent': self.node_is_parent(nd)
        }

    def text_format(self, text, pars):
        """settta pars su text
        vengono coniserati tutti gli elemnti di text dell
        pattern [%][\w.?!+][%] e sono rimpiazzati utilizando il dict pars
        quelli per i quali non vi sono paramteri corrsipondenti
        SONO lasciati nella loro forma originale

        Args:
            text (str): testo con parametri da settare
            pars (dict): parametri per settare text

        Returns:
            str: testo formatato
        """
        ptrn = r"%[\w/,;:.?!^-]+%"
        ms = re.findall(ptrn, text)
        ks = [x.replace('%', '') for x in ms]
        for k in ks:
            v = pars.get(k, f'%{k}%')
            text = text.replace(f'%{k}%', v)
        return text

    def text_format_null(self, text, pars):
        """
        settta pars su text
        vengono coniserati tutti gli elemnti di text selezoinati
        dal pattern [%]\w[%] sono rimpiazzati utilizando il dict pars
        quelli per i quali non vi sono paramteri corrsipondenti
        sono rimossi
        Args:
            text (str): testo con parametri da settare
            pars (dict): parametri per settare text
        Returns:
            str: testo formatato
        """
        ptrn = r"%[\w/,;:.?!^-]+%"
        ms = re.findall(ptrn, text)
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
        """unisce  
            x_data.items 
            csv_data.attrs
            parent x_data.items
            se in csv é settato parent aggiunge parent x_data.iitems
            gli items del parent sono aggiunti con la key composta
            dal tag del parent + la key nella forma parent_key
            es. 
            parent <pb key="valore" ..
            nel iitems esteso del figlio ha la forma
            pb_key=valore
        Args:
            x_data (dict): data estratto da xml
            csv_data (dict): data estartto dat fiele html..:csv
        Returns:
            dict: unione dei due dict
        """
        attrs = {}
        # parent x_data items
        if self.trace:
            # set_trace()
            pass
        csv_tag_parent = csv_data.get('parent', None)
        if csv_tag_parent is not None:
            x_data_parent = self.xml_data_dict.get(csv_tag_parent, None)
            if x_data_parent is not None:
                p_items = x_data_parent.get('items', {})
                # modifica keys di items parent key = <parent>_key
                for k, v in p_items.items():
                    pk = f'{csv_tag_parent}_{k}'
                    attrs[pk] = v
        # x_data items
        x_items = x_data.get('items', {})
        for k, v in x_items.items():
            attrs[k] = v
        # csv_data attrs
        c_attrs = csv_data.get('attrs', {})
        for k, v in c_attrs.items():
            attrs[k] = v
        if self.trace:
            # set_trace()
            pass
        return attrs

    def attrs2html(self, attrs):
        """trasforma in tag htnl attrs 
            ordina partendo da class, id se esistono
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

    def html_attrs_builder(self, x_items, c_keys=[], c_attrs={}):
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
        for k in c_keys:
            attrs[k] = x_items[k]
        for k in c_attrs.keys():
            attrs[k] = c_attrs[k]
        html_attrs = self.attrs2html(attrs)
        return html_attrs

    def get_row_data_info_html(self, x_data):
        """ ritorna dati della row di <tag>.csv individuata
            dall tag o tag+attr di x_data del in xml_data_dict
            la key è quella ottenuta dal tag xml 
            e l'eventuale/i attributo
        Args:
            x_data (dict):xml data
        Returns:
            [row_data (dict): dati estartti da csv
        """
        xml_tag = x_data['tag']
        row_data = self.html_tag_cfg.get(xml_tag, None)
        if row_data is None:
            row_data = self.html_tag_cfg.get('x', {})
            csv_tag = xml_tag
            self.csv_tag_ctrl = f'_x_{csv_tag}'
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
                row_data = self.html_tag_cfg.get(csv_tag, None)
                if row_data is None:
                    row_data = self.html_tag_cfg.get('x+y', None)
                    self.csv_tag_ctrl = f'_xy_{csv_tag}'
                else:
                    self.csv_tag_ctrl = csv_tag
            else:
                csv_tag = xml_tag
                self.csv_tag_ctrl = csv_tag
        self.xml_data_dict[csv_tag] = x_data
        return row_data

    def get_tag_w_last(self):
        """ u
        ltimo tag con id  significativo
        correttamnte utilizzato.
        In caso di errore + l'ultimo tag corretto
        """        
        tag_w_last = ''
        le = len(self.hb.get_tag_lst())
        if le == 0:
            return ""
        x = 5 if le > 5 else le
        for i in range(1, x):
            tag_w_last = self.hb.get_tag_lst()[-i:][0].strip()
            if tag_w_last.find('id') > -1:
                break
        return tag_w_last

    def build_html_tag(self, x_data):
        """raccogli i dati per costruire un elemnt html
        Args:
            x_data (dict): dati presi da xml
        Returns:
            dict: dati necessari a costruire html
        """
        x_items = x_data['items']
        x_text = x_data['text']
        x_tail = x_data['tail']
        x_liv = x_data['liv']
        self.is_container_stack[x_liv] = False
        c_data = self. get_row_data_info_html(x_data)
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
        # unisce x_items selezionato da c_keys + c_attrs
        html_attrs = self.html_attrs_builder(x_items, c_keys, c_attrs)
        #
        # dic esteso x_dta + c_data è parent.x_dta
        ext_items = self.items_extend(x_data, c_data)
        if html_attrs.find('%') > -1:
            # rimpiazza se esiste %text% con x_data['text']
            if html_attrs.find('%text%') > -1:
                html_attrs = html_attrs.replace('%text%', x_text)
            # setta parametri utilizzando c_params
            # sono lascait quelli senza corrsipondenti
            html_attrs = self.text_format(html_attrs, c_params)
            # setta parametri attr. elimina quelli che non hanno corrisponedenti
            html_attrs = self.text_format_null(html_attrs, x_items)
            html_attrs = self.class_adjust(html_attrs)
        #
        # formatta c_text itilizzando ext_items :items + parent.items)
        if c_text.find('%') > -1:
            c_text = self.text_format(c_text, ext_items)
            # formatta c_text con %text% se esiste elimina x_text
            if c_text.find('%text%') > -1:
                if x_data.get('is_parent', None) is False:
                    c_text = c_text.replace('%text%', x_text)
                    x_text = ''
                else:
                    self.is_container_stack[x_liv] = True
            # setta c_text utilizzando c_params
            if c_text.find('%') > -1:
                c_text = self.text_format(c_text, c_params)
        #
        html_text = x_text+c_text
        ####################
        html_data = {
            'tag': c_tag,
            'attrs': html_attrs,
            'text': html_text,
            'tail':x_tail
        }
        # ERRORi nella gestione del files csv dei tag html
        if self.csv_tag_ctrl.find('_x') > -1:
            logcsverr.log(f"ERROR in csv tag:{self.csv_tag_ctrl}").prn()
            logcsverr.log(f"file: {self.xml_path}").prn()
            logcsverr.log("xml:", pp(x_data)).prn()
            logcsverr.log("csv:", self.csv_tag_ctrl).prn()
            logcsverr.log("ext_items:", pp(ext_items)).prn()
            logcsverr.log("html:", pp(html_data)).prn()
            # ultimo tag w prima dell'ERRORe
            tag_w_last = self.get_tag_w_last()
            logcsverr.log("last w: ", tag_w_last).prn()
            logcsverr.log(os.linesep).prn()
            inp.inp("!")
        ################################
        if inp.prn:
            loginfo.log(">> html_data").prn()
            loginfo.log(pp(html_data)).prn()
            loginfo.log(">> ext_items").prn()
            loginfo.log(pp(ext_items)).prn()
        ################################
        # TODO valutare se exit/1) al verificarsi dell'errore
        # sys.exit(1)
        return html_data

    def set_pc(self, x_data):
        if x_data['tag'] == 'pc':
            t=x_data['text'].strip()
            if t in ['.','?','!']:
                self.pc_active = True

    def after_pc(self, x_data,h_data,text,tail):
        if self.trace:
            # set_trace()
            pass
        liv=x_data['liv']
        tag=x_data['tag']
        if tag =='w':
            self.w_liv=liv
            if text.strip()!='':
                text='X'+text
                self.pc_active=False  
                self.w_liv=100
        h_tag=h_data['tag']
        if liv > self.w_liv and h_tag !='XXX':
            if text.strip()!='':
                text='X'+text
                self.pc_active=False  
                self.w_liv=100
            elif tail.strip()!='':
                tail='Y'+tail
                self.pc_active=False  
                self.w_liv=100
        return text,tail

    def html_append(self, nd):
        """
        estrae da nd x_data
        invoca build_html_tah()
        setta:h_data
        utilizza self.hb (HtmlBuildr) per costruire HTML
        Args:
            nd (xml.node): nodo xml
        """
        x_data = self.get_node_data(nd)

        if self.dipl_inter=='d':
            if x_data['id']=="Gl12w4":
                self.trace=True

        # aggiorna xml_data_lst da utilzzare per HtmlOverflow
        self.xml_data_lst.append(x_data)
        x_liv = x_data['liv']
        x_is_parent = x_data['is_parent']
        x_tag = x_data['tag']
        # setta dati per tag html
        h_data = self.build_html_tag(x_data)
        h_tag = h_data['tag']
        h_text = h_data['text']
        h_tail = h_data['tail']
        h_attrs = h_data['attrs']
        # se il precedente è un parent contenitor
        prev_is_container = self.is_container_stack[x_liv-1]
        if prev_is_container:
            # rimpiazza text  nel tag precdente (il container)
            content = f'<{h_tag} {h_attrs}>{h_text}</{h_tag}>{h_tail}'
            s = self.hb.tag_last()
            content = s.replace('%text%', content)
            self.hb.upd_tag_last(content)
            # setta con XXX perrimuovere da aggiungere in quanto
            # è stato inserito nel contente del parent
            h_tag = 'XXX'
        # gestione interpretativa
        if self.dipl_inter == 'i':
            h_text = h_text.lower()
            h_tail = h_tail.lower()
            self.set_pc(x_data)
            if self.pc_active:
                h_text,h_tail=self.after_pc(x_data,h_data,h_text,h_tail)

        if x_is_parent:
            self.hb.opn(x_liv, h_tag, h_attrs, h_text, h_tail)
        else:
            self.hb.ovc(x_liv, h_tag, h_attrs, h_text, h_tail)
        if inp.prn:
            loginfo.log(">> html node").prn(1)
            loginfo.log(self.hb.tag_last()).prn(1)
        inp.inp(x_tag)
        if inp.equals('?'):
            print(self.hb.html_format())
            inp.inp()

    def set_html_pramas(self, html):
        """utilizzando il file json formatta i parametri residui
            es. il nome del manoscrittp _MAN_
            qualsiasi altro parametro definito nel file cid configurazione
            al tag html_params
        Args:
            html (str): html 
        Returns:
            html (str): html con settati i parametri         """
        params = self.html_cfg.get("html_params", {})
        for k, v in params.items():
            html = html.replace(k, v)
        return html

    def check_tml(self):
        """ controlla tutte le righe htnl di HtmlBuilder
        per verificare che vi sda qualche parametro
        del tipo %param% non settato
        """
        ptrn = r"%[\w/,;:.?!^-]+%"
        rows = self.hb.get_tag_lst()
        le = len(rows)
        for i, row in enumerate(rows):
            ms = re.search(ptrn, row)
            if ms is not None:
                loghtmlerr.log(f"ERROR nel parametro: {ms.group()}").prn()
                loghtmlerr.log(f"file: {self.xml_path}")
                if i > 3:
                    loghtmlerr.log(rows[i-3].strip()).prn()
                if i > 2:
                    loghtmlerr.log(rows[i-2].strip()).prn()
                if i > 1:
                    loghtmlerr.log(rows[i-1].strip()).prn()
                loghtmlerr.log("**")
                loghtmlerr.log("     "+row.strip()).prn()
                loghtmlerr.log("**")
                if i < le-2:
                    loghtmlerr.log(rows[i+1].strip()).prn()
                if i < le-3:
                    loghtmlerr.log(rows[i+2].strip()).prn()
                if i < le-4:
                    loghtmlerr.log(rows[i+3].strip()).prn()

                #tag_w_last = self.get_tag_w_last()
                #loghtmlerr.log("last w: ", tag_w_last).prn()

                loghtmlerr.log(os.linesep).prn()
                inp.inp('!')
                # TODO valutare se exit/1) al verificarsi dell'errore
                # sys.exit(1)

    def read_conf(self, json_path):
        try:
            self.html_cfg = read_json(json_path)
            logconf.log(pp(self.html_cfg).replace("'", '"')).prn(0)
            #
            # hrml dipl./inter
            self.dipl_inter = self.html_cfg.get("dipl_inter", None)
            if self.dipl_inter is None or self.dipl_inter not in ['d', 'i']:
                raise Exception(f"ERROR dipl_inter: {self.dipl_inter}")
            #
            # prefisso di  id per diplomatia e interpretativa
            self.before_id = self.html_cfg.get("before_id", None)
            if self.before_id is None:
                raise Exception("ERROR before_id is null.")
            #
            csv_path = self.html_cfg.get("html_tag_file", None)
            if csv_path is None:
                raise Exception("ERROR html_tag_file is null.")
            #
            # type : d:txt d:syn i:txt i:syn
            html_tag_type = self.html_cfg.get("html_tag_type", None)
            if html_tag_type is None:
                raise Exception("ERROR html_tag_type is null.")
            self.html_tag_cfg = read_html_conf(csv_path, html_tag_type)
            logconf.log(pp(self.html_tag_cfg).replace("'", '"')).prn(0)
        except Exception as e:
            logerr.log("ERROR: read_conf())")
            logerr.log(e)
            sys.exit(1)

    def write_html(self, xml_path, html_path, json_path, write_append='w', debug_liv='0'):
        """fa il parse del file xml_path scrive i files:
            nel formato comapatto: <html_path>
            formato indentato <html_name>_f.html
        Args:
            xml_path (str]:  file xml
            html_path (str): file html
            json_path (str): file di configurazoine
            write_append(str): modalità output
            deb (bool, optional): flag per gestione debuf
        Returns:
            html_path (str): filr name html 
        """
        try:
            inp.set(debug_liv)
            self.xml_data_lst = []
            self.xml_path = xml_path
            self.html_path = html_path
            if write_append not in ['w', 'a']:
                raise Exception(
                    f"ERROR in output write/append. {write_append}")
            # lettur a file configurazione
            self.read_conf(json_path)
            # lib per costruziona html
            self.hb = HtmlBuilder()
            # dict dei dati xml con tag come key
            self.xml_data_dict = {}
            # stack dei nodi che sono si/no container
            self.is_container_stack = [False for i in range(1, 20)]
            # tag per controlo ERRORi
            self.csv_tag_ctrl = ""
            #
            self.hb.init()
            try:
                xml_root = etree.parse(self.xml_path)
            except Exception as e:
                logerr.log("ERROR teixml2html.py write_html() parse_xml")
                logerr.log(e)
                sys.exit(1)
            for nd in xml_root.iter():
                self.html_append(nd)
            self.hb.del_tags('XXX')
            self.hb.end()
            """gestisce il settaggio degli overflow
            modifica il parametro html_lst
            Returns:
                str: html modificato
            """
            html_lst = self.hb.get_tag_lst()
            html_over = HtmlOvweflow(
                self.xml_data_lst, html_lst, self.html_tag_cfg)
            html_over.set_overflow()
            # controllo dei parametri %par% non settati
            self.check_tml()
            # html su una riga versione per produzione
            html = self.hb.html_onerow()
            html = self.set_html_pramas(html)
            with open(self.html_path, write_append) as f:
                f.write(html)
            os.chmod(self.html_path, 0o666)
        except Exception as e:
            logerr.log("ERROR teixml2html.py write_html()")
            logerr.log(e)
            sys.exit(1)
        return self.html_path


def do_mauin(xml, html, conf, wa='w', deb=False):
    Xml2Html().write_html(xml, html, conf, wa, deb)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    if len(sys.argv) == 1:
        print("release: %s  %s" % (__version__, __date__))
        parser.print_help()
        sys.exit(1)
    parser.add_argument('-d',
                        dest="deb",
                        required=False,
                        metavar="",
                        default=0,
                        help="[-d 0/1/2](setta livello di debug)")
    parser.add_argument('-wa',
                        dest="wa",
                        required=False,
                        metavar="",
                        default="w",
                        help="[-wa w/a (w)rite a)ppend) default w")
    parser.add_argument('-c',
                        dest="cfg",
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
    do_mauin(args.xml, args.html, args.cfg, args.wa, args.deb)
