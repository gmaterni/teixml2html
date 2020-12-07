#!/bin/bash

xml_path="xml/ven/ep21.xml"
html_path="html/ADvdenep21.html"

csv_path="cnf/htmltagsdip.csv"
json_path="cnf/htmlconf.json"

teixml2html.py ${xml_path} ${html_path} ${csv_path} ${json_path}
