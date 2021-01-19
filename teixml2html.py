#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pdb import set_trace
import os
import re
from lxml import etree
import pprint
import sys
import argparse
from readhtmlconf import read_html_conf
from readjson import read_json
from htmlbuilder import HtmlBuilder
from htmloverflow import HtmlOvweflow
from ualog import Log
from uainput import Inp

__date__ = "15-01-2021"
__version__ = "0.3.0"
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
inp = Inp()


class Xml2Html:

    def __init__(self):
        logconf.open("log/cgf.json", 0)
        loginfo.open("log/teixml2html.log", 0)
        logerr.open("log/teixml2html.ERR.log", 1)
        logcsverr.open("log/csv.ERR.log", 1)
        loghtmlerr.open("log/html.ERR.log", 1)
        self.xml_path = None
        self.html_path = None
        self.info_params = None
        self.info_html_tags = None
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
        # tag di controllo per erroi csv
        self.csv_tag_ctrl = None
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
            'tag': self.node_tag(nd).lower(),
            'tail': self.node_tail(nd),
            'text': self.node_text(nd),
            'items': items,
            # 'keys': self.node_keys(nd),
            # 'val':self.node_val(nd),
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
        """settta pars su text
        vengono coniserati tutti gli elemnti di text dell
        pattern [%]\w[%] e sono rimpiazzati utilizando il dict pars
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
            se in csv é settato parent aggiunge 
            parent x_data.iitems
            gli items del parent sono aggiunti con la key compostaù
            dal tag del parent + la key.
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
        csv_tag_parent = csv_data.get('parent', None)
        if csv_tag_parent is not None:
            x_data_parent = self.xml_data_dict.get(csv_tag_parent, None)
            if x_data_parent is not None:
                p_items = x_data_parent.get('items', {})
                # modifica keys di items parent
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
        for k in c_keys:
            attrs[k] = x_items[k]
        for k in c_attrs.keys():
            attrs[k] = c_attrs[k]
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

    def get_row_data_info_html(self, x_data):
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
        row_data = self.info_html_tags.get(xml_tag, None)
        if row_data is None:
            row_data = self.info_html_tags.get('x', {})
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
                row_data = self.info_html_tags.get(csv_tag, None)
                if row_data is None:
                    row_data = self.info_html_tags.get('x+y', None)
                    self.csv_tag_ctrl = f'_xy_{csv_tag}'
                else:
                    self.csv_tag_ctrl = csv_tag
            else:
                csv_tag = xml_tag
                self.csv_tag_ctrl = csv_tag
        self.xml_data_dict[csv_tag] = x_data
        return row_data

    def build_content(self, tag, attrs, text, tail):
        t = f'<{tag} {attrs}>{text}</{tag}>{tail}'
        return t

    def  get_tag_w_last(self):
        tag_w_last = ''
        le=len(self.hb.get_tag_lst())
        if le==0:
            return ""
        x= 5 if le > 5 else le
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
        # dice selezionato da c_keys
        html_attrs = self.attrs_builder(x_items, c_keys, c_attrs)
        h_attrs_str = self.attrs2html(html_attrs)
        #
        ext_items = self.items_extend(x_data, c_data)
        """
        if x_data['tag'] == 'pc':
            # set_trace()
            self.trace=True
        """
        if h_attrs_str.find('%') > -1:
            # rimpiazza se esiste %text% con x_data['text']
            if h_attrs_str.find('%text%') > -1:
                h_attrs_str = h_attrs_str.replace('%text%', x_text)
            # formatta utilizzando x_params, sono lascait qyelli senza corrsipondenti
            h_attrs_str = self.text_format(h_attrs_str, c_params)
            # formatta attr (x_items [solo c_keys) ] + c_attr)
            h_attrs_str = self.text_format_null(h_attrs_str, x_items)
            h_attrs_str = self.class_adjust(h_attrs_str)
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
            # formatta c_text utilizzando c_params
            if c_text.find('%') > -1:
                c_text = self.text_format(c_text, c_params)
        #
        html_text = x_text+c_text
        ####################
        html_data = {
            'tag': c_tag,
            'attrs': h_attrs_str,
            'text': html_text
        }
        # ERRORi nella gestione del files csv dei tag html
        if self.csv_tag_ctrl.find('_x') > -1 :
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
        return html_data

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
        # aggiorna xml_data_lst da utilzzare per HtmlOverflow
        self.xml_data_lst.append(x_data)
        x_tag = x_data['tag']
        x_liv = x_data['liv']
        x_is_parent = x_data['is_parent']
        x_tail = x_data['tail']
        # setta dati per tag html
        h_data = self.build_html_tag(x_data)
        h_tag = h_data['tag']
        h_text = h_data['text']
        h_attrs = h_data['attrs']
        # se il precedente è un parent contenitor
        prev_is_container = self.is_container_stack[x_liv-1]
        if prev_is_container:
            # rimpiazza text  nel tag precdente (il container)
            content = self.build_content(h_tag, h_attrs, h_text, x_tail)
            s = self.hb.tag_last()
            content = s.replace('%text%', content)
            self.hb.upd_tag_last(content)
            #
            # setta con XXX perrimuovere da aggiungere in quanto
            # è stato inserito nel contente del parent
            h_tag = 'XXX'
        if x_is_parent:
            self.hb.opn(x_liv, h_tag, h_attrs, h_text, x_tail)
        else:
            self.hb.ovc(x_liv, h_tag, h_attrs, h_text, x_tail)
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
        params = self.info_params.get("html_params", {})
        for k, v in params.items():
            html = html.replace(k, v)
        return html

    def check_tml(self):
        """ controlla tutte le righe htnl di HtmlBuilder
        per verificare che vi sda qualche parametro
        del tipo %param% non settato
        """        
        ptrn = r"%[\w/,;:.?!^-]+%"
        rows =self.hb.get_tag_lst()
        for row in rows:
            ms = re.search(ptrn, row)
            if ms is not None:
                loghtmlerr.log( f"ERROR nel parametro: {ms.group()}").prn()
                loghtmlerr.log(f"file: {self.xml_path}")
                loghtmlerr.log(row.strip()).prn()
                # ultimo tag w prima dell'ERRORe
                tag_w_last = self.get_tag_w_last()
                loghtmlerr.log("last w: ", tag_w_last).prn()
                loghtmlerr.log(os.linesep).prn()
                inp.inp('!')

    
    def read_conf(self, json_path):
        try:
            self.info_params = read_json(json_path)
            logconf.log(pp(self.info_params).replace("'", '"')).prn(0)
            # prefisso di  id per diplomatia e interpretativa
            self.before_id = self.info_params.get("before_id", None)
            if self.before_id is None:
                raise Exception(f"ERROR before_id is null.")
            #
            csv_path = self.info_params.get("html_info", None)
            if csv_path is None:
                raise Exception("ERROR csv_path is null.")
            html_type = self.info_params.get("html_type", None)
            if html_type is None:
                raise Exception("ERROR html_type is null.")
            self.info_html_tags = read_html_conf(csv_path, html_type)
            logconf.log(pp(self.info_html_tags).replace("'", '"')).prn(0)
        except Exception as e:
            logerr.log(os.linesep, "ERROR: read_conf())")
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
        inp.set(debug_liv)
        self.xml_data_lst = []
        self.xml_path = xml_path
        self.html_path = html_path
        write_append = write_append.lower()
        if write_append not in ['w', 'a']:
            raise Exception(f"ERROR in output write/append. {write_append}")
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
            logerr.log("ERROR teixml2html.py write_html()")
            logerr.log(e)
            sys.exit(1)
        for nd in xml_root.iter():
            self.html_append(nd)
        self.hb.del_tags('XXX')
        self.hb.end()
        #############################
        """gestisce il settaggio degli overflow
        modifica il parametro html_lst
        Returns:
            str: html modificato
        """
        html_lst = self.hb.get_tag_lst()
        html_over = HtmlOvweflow(
            self.xml_data_lst, html_lst, self.info_html_tags)
        html_over.set_overflow()
        # controllo dei parametri %par% non settati
        self.check_tml()
        # html su una riga versione per produzione
        html = self.hb.html_onerow()
        html = self.set_html_pramas(html)
        with open(self.html_path, write_append) as f:
            f.write(html)
        os.chmod(self.html_path, 0o666)
        #
        # html formattato versione per il debug
        # file_name.html => file_name_X.html
        """
        if int(debug_liv)> 0:
            html = self.hb.html_format()
            html = self.set_html_pramas(html)
            path = self.html_path.replace(".html", "_F.html")
            with open(path, write_append) as f:
                f.write(html)
            os.chmod(self.html_path, 0o666)
        """
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
                        dest="cgf",
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
        sys.exit(1)
    do_mauin(args.xml, args.html, args.cgf, args.wa, args.deb)
