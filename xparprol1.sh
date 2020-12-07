#!/bin/bash

xml_path="xml/tor/prol1.xml"
html_path="html/ADparprol1.html"

csv_path="cnf/htmltagsdip.csv"
json_path="cnf/htmlconf.json"

teixml2html.py -i ${xml_path} -o ${html_path} -t ${csv_path} -c ${json_path}
