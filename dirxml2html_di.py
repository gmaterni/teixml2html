#!/usr/bin/env python
import os
import sys

def do_main(xml_dir,html_dir):
    csvd=f"cnf/htmldipl.csv"
    csvi=f"cnf/htmlinter.csv"
    for f in os.listdir(xml_dir):
        xml=os.path.join(xml_dir,f)
        if os.path.isfile(xml) is False:
            continue
        xml_name=os.path.basename(xml)
        if xml_name.endswith('xml') is False:
            continue
        html_name=xml_name.replace('.xml','.html')
        html_path=os.path.join(html_dir,html_name)
        #
        dir_name_xml=os.path.dirname(xml)
        mano=dir_name_xml.split('/')[-1:][0]  
        json=f"cnf/{mano}.json"
        print(xml)
        prg=f"teixml2html_di.py -i {xml} -o {html_path} -td {csvd} -ti {csvi} -c {json}"
        rt = os.system(prg)
        if rt != 0:
            sys.exit()

if __name__ == '__main__':
    if len(sys.argv)==1:
        print("xml_path html_path")
        sys.exit()
    xml_dir=sys.argv[1]
    html_dir=sys.argv[2]
    do_main(xml_dir,html_dir)

