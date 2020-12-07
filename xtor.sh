#!/bin/bash

xml_path="xml/tor/tor.xml"
html_path="html/ADtor.html"

csv_path="cnf/htmltagsdip.csv"
json_path="cnf/htmlconf.json"

teixml2html.py -i ${xml_path} -o ${html_path} -t ${csv_path} -c ${json_path}
