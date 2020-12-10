#!/usr/bin/env python
import os
import sys


def do_main(dr,dip_int):
    # cwd = os.getcwd()
    di='dipl' if dip_int=='d' else 'inter'
    csv=f"cnf/html{di}.csv"
    for f in os.listdir(dr):
        xml=os.path.join(dr,f)
        if os.path.isfile(xml) is False:
            continue
        xml_name=os.path.basename(xml)
        if xml_name.endswith('xml') is False:
            continue
        s=xml_name.replace('.xml','.html')
        x=os.path.dirname(xml)
        mano=x.split('/')[-1:][0]  
        html_name=f'A{dip_int}{mano}_{s}'
        html=os.path.join("html/x",html_name)
        #
        json=f"cnf/{mano}{di}.json"
        print(xml)
        prg=f"teixml2html.py -i {xml} -o {html} -t {csv} -c {json}"
        rt = os.system(prg)
        if rt != 0:
            sys.exit()

if __name__ == '__main__':
    d=sys.argv[1]
    dip_int=sys.argv[2]
    do_main(d,dip_int)

