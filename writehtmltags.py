#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import copy
from lxml import etree

 
class WriteHtmlTags(object):

    def __init__(self, path_src,path_nhtags):
        self.path_src = path_src
        self.path_nhtags=path_nhtags
    
    def node_liv(self, nd):
        d = 0
        while nd is not None:
            d += 1
            nd = nd.getparent()
        return d - 1
    

    def node_tag(self, nd):
        tag = nd.tag if type(nd.tag) is str else "XXX_no_tag"
        # _XXX_ quando succede ?
        pid = tag.find('}')
        if pid > 0:
            tag = tag[pid + 1:]
        return tag.strip()

    def node_text(self, nd):
        text = "" if nd.text is None else nd.text
        s = text.replace(os.linesep, '', -1)
        return s.strip()

    def node_tail(self, nd):
        tail = "" if nd.tail is None else nd.tail
        s = tail.replace(os.linesep, '', -1)
        return s.strip()

    # {'k0':v0,'k1':v1,..}  pulisce  id come key
    def node_attrjs(self, nd):
        attrs = {}
        if nd.attrib is None:
            return attrs
        for k, v in nd.attrib.iteritems():
            px = k.find('}')
            if px > -1:
                k = k[px + 1:]
            attrs[k] = v
        return attrs

    # [('k0','v0'),('k1','v1')] ordinato per key
    # salta id
    def node_attr_lsT(self, nd):
        attrs = self.node_attrjs(nd)
        if attrs == {}:
            return []
        ks = attrs.keys()
        kss = sorted(ks)
        ls = []
        for k in kss:
            if k == 'id':
                continue
            v = attrs[k]
            ls.append([k, v])
        return ls
    
    def htaks_key1(self, tagls):
        s = ':'.join(tagls)
        return s
    
    # v0:v1:v2 escluso pe k in ['n','x']
    # salta  n
    def htags_key2(self, attrls):
        ls = []
        for attr in attrls:
            kv = attr
            k = kv[0]
            v = kv[1]
            if k in ['n']:
                continue
            ls.append(v)
        lss = sorted(ls)
        attrsv = ':'.join(lss)
        return attrsv
    
    
    def node_id(self, nd):
        attrs = self.node_attrjs(nd)
        vid = attrs.get('id', "")
        return vid.strip()
    
    def node_parent(self, nd):
        ndp = nd.getparent()
        return ndp
    
    # gestisce lo stack dei tag in funzione del livello
    def set_stack_liv(self, stk, tag, liv):
        le = len(stk)
        # loginfo3.log("%s  %s  %s %s " % (str(stk), le ,tag, liv))
        # lv = liv + 1
        if liv == 0:
            return [tag]
        lv = liv
        if lv > le:
            stk.append(tag)
        elif lv == le:
            stk[le - 1] = tag
        else:
            stk = stk[:lv - le]
            la = len(stk) - 1
            stk[la] = tag
        # loginfo3.log("%s  %s  %s" % (str(stk),len(stk),os.linesep))
        return stk
       

    
    def build_wjs(self, nd):

        # trasforma una lista di lste in una lista
        def _stk2lst(stk):
            lst = []
            for ls in stk:
                for x in ls:
                    lst.append(x)
            return lst

        id = self.node_id(nd)
        tag = self.node_tag(nd)
        text = self.node_text(nd)
        tail = self.node_tail(nd)
        liv = self.node_liv(nd)
        attrls = self.node_attr_lsT(nd)

        tagstk = [tag]
        attrstk = [attrls]
        for a in nd.iterancestors():
            tg = self.node_tag(a)
            attrls = self.node_attr_lsT(a)
            if tg == 'l':
                break
            tagstk.insert(0, tg)
            attrstk.insert(0, attrls)
        attrstke = _stk2lst(attrstk)

        dls = []
        for d in nd.iterchildren():
            tg = self.node_tag(d)
            dls.append(tg)

        wjs = {
            'id': id,
            'tag': tag,
            'text': text,
            'liv': liv,
            'tail': tail,
            'tagstk': tagstk,
            'attrstk': attrstke,
            'childr': dls
        }
        return wjs
    
    
    def node_line_data(self, lnd):
        lid = self.node_id(lnd)
        ldata = {'id': lid}
        wjsls = []
        wt = None
        wjs = None
        for nd in lnd.iterdescendants():
            if wt is not None:
                liv = self.node_liv(nd)
                tliv = wt['liv']
                if liv <= tliv:
                    w = copy.deepcopy(wt)
                    wjsls.append(w)
                    wt = None
            wjs = self.build_wjs(nd)
            w = copy.deepcopy(wjs)
            wjsls.append(w)
            if wt is not None:
                w = copy.deepcopy(wt)
                wjsls.append(w)
                wt = None
            tail = self.node_tail(nd)
            if tail != '':
                np = self.node_parent(nd)
                w = self.build_wjs(np)
                wt = copy.deepcopy(w)
                wt['childr'] = []
                wt['text'] = tail
        if wt is not None:
            wjsls.append(wt)
        # elimina i tag con testp vuotp
        ls = [x for x in wjsls if x['text'] != '']
        # eliminazione id duolicati
        idls = []
        for wjs in ls:
            id = wjs['id']
            if id == '':
                continue
            if id in idls:
                wjs['id'] = ''
            else:
                idls.append(id)
        ldata['wjsls'] = ls
        return ldata
    
    def write_html_tags_csv(self):
        
        def set_class(tag, tagstk):
            if tag == 'pc':
                cls = 'pc'                
                return cls

            t0 = tagstk[0]
            le = len(tagstk)
            if t0 == 'w':
                cls = 'w'
                if le > 1:
                    cls = "w e"
            elif t0 == 'seg':
                cls = 'seg'
                if le > 1:
                    cls = 'seg w'
                if le > 2:
                    cls = 'seg w e'
            else:
                cls = 'x'
            return cls

        stack_liv = []
        root = etree.parse(self.path_src)
        ls0 = []
        for nd in root.iter():
            tag = self.node_tag(nd)
            liv = self.node_liv(nd)
            stack_liv = self.set_stack_liv(stack_liv, tag, liv)
            line_liv = stack_liv.index('l') if 'l' in stack_liv else -1

            # i tag parenti di l
            if line_liv < 0:
                # attr_lst = self.node_attr_lsT(nd)
                # k2 = self.htags_key2(attr_lst)
                k2 = ""
                cls = tag
                if tag == 'pb':
                    s = '%s|%s|<div id="${id}" class="%s" />' % (tag, k2, cls)
                elif tag == 'cb':
                    s = '%s|%s|<div id="${id}" class="%s" />' % (tag, k2, cls)
                elif tag == 'span':
                    # from to
                    s = '%s|%s|<span  from="${from}" to="${to}" />' % (tag, k2)
                elif tag == 'lg':
                    s = '%s|%s|<div id="${id}" n="${n}" class="%s" >' % (tag, k2, cls)
                elif tag == 'div':
                    s = '%s|%s|<div  class="%s" >' % (tag, k2, cls)
                else:
                    s = '%s|%s|<div  class="%s" />' % (tag, k2, cls)
                # print(s)
                ls0.append(s)
                continue

            if tag == 'l':
                # attr_lst = self.node_attr_lsT(nd)
                # k2 = self.htags_key2(attr_lst)
                k2 = ""
                cls = tag
                s = '%s|%s|<div id="${id}" n="${n}" class="%s">' % (tag, k2, cls)
                ls0.append(s)
                # elementi linea
                ldata = self.node_line_data(nd)
                wjsls = ldata['wjsls']
                for wjs in wjsls:
                    tag = wjs['tag']
                    tagstk = wjs['tagstk']
                    k1 = self.htaks_key1(tagstk)
                    # attrstk = wjs['attrstk']
                    # k2 = self.htags_key2(attrstk)
                    k2 = ""
                    # cls = k1.replace(":", "_", -1)
                    cls = set_class(tag, tagstk)
                    if k1 == ' w':
                        s = '%s|%s|<div id="${id}" class="%s">${text}</div> ' % (k1, k2, cls)
                    elif k1 == 'pc':
                        s = '%s|%s|<div id="${id}" class="%s">${text}</div> ' % (k1, k2, cls)
                    else:
                        s = '%s|%s|<div id="${id}" class="%s">${text}</div> ' % (k1, k2, cls)
                    # print(s)
                    ls0.append(s)

        ls2 = sorted(list(set(ls0)))
        with open(self.path_nhtags, 'w+') as f:
            for x in ls2:
                f.write(x)
                f.write(os.linesep)
        os.chmod(self.path_nhtags, 0o666)



def do_main():
    src="xml/tor/floritor.xml"
    tagnew="csv/tags_tor.csv"
    WriteHtmlTags(src, tagnew).write_html_tags_csv()

if __name__ == "__main__":    
    do_main()

