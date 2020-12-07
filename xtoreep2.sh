#!/bin/bash


xml_path="xml/tor/ep2.xml"
html_path="html/ADtorep2.html"

csv_path="cnf/htmltagsdip.csv"
json_path="cnf/htmlconf.json"

teixml2html.py -i ${xml_path} -o ${html_path} -t ${csv_path} -c ${json_path}
