#!/usr/bin/env python
import os
import sys

def do_main(xml_dir,html_dir,dip_int):
    di='dipl' if dip_int=='d' else 'inter'
    csv=f"cnf/html{di}.csv"
    for f in os.listdir(xml_dir):
        xml=os.path.join(xml_dir,f)
        if os.path.isfile(xml) is False:
            continue
        xml_name=os.path.basename(xml)
        if xml_name.endswith('xml') is False:
            continue
        html_name=xml_name.replace('.xml',f'{dip_int}.html')
        html_path=os.path.join(html_dir,html_name)
        #
        dir_name_xml=os.path.dirname(xml)
        mano=dir_name_xml.split('/')[-1:][0]  
        json=f"cnf/{mano}.json"
        print(xml)
        prg=f"teixml2html.py -i {xml} -o {html_path} -t {csv} -c {json}"
        rt = os.system(prg)
        if rt != 0:
            sys.exit()

if __name__ == '__main__':
    if len(sys.argv)==1:
        print("xml_path html_path d/i")
        sys.exit()
    xml_dir=sys.argv[1]
    html_dir=sys.argv[2]
    dip_int=sys.argv[3]
    do_main(xml_dir,html_dir,dip_int)

