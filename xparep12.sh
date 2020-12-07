#!/bin/bash

xml=x"ml/par/ep12.xml"
html="./html/ADparep12.html"

csv="cnf/htmltagsdip.csv"
json="cnf/htmlconf.json"

teixml2html.py -i ${xml} -o ${html} -t ${csv} -c ${json} -d
