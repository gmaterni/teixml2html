#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pdb import set_trace
from ualog import Log
import pprint
import os
import sys

def pp(data):
    if data is None:
        return ""
    s = pprint.pformat(data, indent=2, width=120)
    return s+os.linesep


logerr = Log("a")


class HtmlOvweflow(object):
    """gestisce propriet+ overflov
    utilizzando <span from="<id>" to="<id>"  type0"<tipo>" 

    """
    def __init__(self, xml_lst, html_lst, html_conf):
        """gestione overflow

        Args:
            xml_lst (list): lista dei dati xml
            html_lst (lis): lista delle righe html
            html_conf (dict): dict del fie di configurazione csv
        """        
        logerr.open("log/htmloverflow.err.log", 1)
        self.xml_lst = xml_lst
        self.html_lst = html_lst
        self.html_conf=html_conf
        self.span_lst = []
        self.cls_w='class="w'
        self.cls_pc='class="pc'

    def fill_span_list(self):
        for x_data in self.xml_lst:
            x_tag = x_data.get('tag', '')
            if x_tag == 'span':
                x_items = x_data.get('items', {})
                x_from = x_items.get('from', None)
                x_to = x_items.get('to', None)
                x_type = x_items.get('type', None)
                if x_from is None or x_to is None or x_type is None:
                    logerr.log("fill_span_list ERROR.").prn()
                    logerr.log(pp(x_data).prn())
                    sys.exit()
                item = {
                    "id0": x_from,
                    "id1": x_to,
                    "type": x_type
                }
                self.span_lst.append(item)

    # tei_direct_beg_int  
    # tei_episode_beg_int
    def add_html_class(self, flg, rh, tp):
        """ aggiunge una classe alle righe html in funzione del flag
        e del type
        <span from="Gl23w1" to="Gl98w6" type="directspeech"/>
        modifica da from a to secondo typt
                <div class="w aggl-s" id="dGl2w1">Si</div>s
        <span class="pc_ed" id="dGl44pc1">,</span>

        Args:
            flg (int):  flga per inizio e fine intervallo
            rh (str): riga html
            tp (str): tipo span from to

        Returns:
            str: riga html odificata
        """
        try:
            c_data=self.html_conf.get(tp,None)
            if c_data is None:
                raise Exception(f"type:{tp} Error in find csv")
            clazz=c_data.get('tag',None)
            if clazz is None :
                raise Exception(f"type:{tp} Error tag in csv")
            if flg == 0:
                cls = f"beg_{clazz}"
            elif flg == 2:
                cls = f"end_{clazz}"
            else:
                cls = clazz
            p0=rh.find(self.cls_w)
            if p0 > -1:
                p0=p0+len(self.cls_w)
            else:
                p0=rh.find(self.cls_pc  )
                p0=p0+len(self.cls_pc)
            if p0 < 0:
                raise Exception("Error in html")
            p1=rh.find('"',p0)
            s=rh[0:p1]+" "+cls+rh[p1:]
            return s
        except Exception as e:
            logerr.log(e)
            logerr.log(rh)
            sys.exit()


    def find_w_id(self,r,id):
        ptr_id=f'{id}"'
        p=r.find(ptr_id)
        return p > -1
    
    def find_w_pc(self,rh):
        p= rh.find(self.cls_w)
        if p < 0:
            p= rh.find(self.cls_pc)
        return p > -1

    def set_html(self,from_to):
        """setta le righe html comprese nellìintervallo from to

        Args:
            from_to (str): intervallo degli id delle classi w e pc
        """
        id0=from_to['id0']
        id1=from_to['id1']
        tp=from_to['type']
        flag = 0
        for i,rh in enumerate(self.html_lst):
            if flag==0:
                if self.find_w_pc(rh):
                    if self.find_w_id(rh,id0) :
                        row=self.add_html_class(0,rh,tp)
                        self.html_lst[i]=row
                        flag=1
                        continue
            if flag==1:
                if self.find_w_pc(rh):
                    if self.find_w_id(rh,id1):
                        row=self.add_html_class(2,rh,tp)
                        self.html_lst[i]=row
                        flag=3
                        break
                    row=self.add_html_class(1,rh,tp)
                    self.html_lst[i]=row
        if flag==0:
            logerr.log(f"{id0} {id1}  {tp}   Not Found")
                

    def set_overflow(self):
        self.fill_span_list()
        for x_data in self.span_lst:
            self.set_html(x_data)
