#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from readhtmlconf import read_html_conf
import json


def do_main(csv_path, json_path):
    csv = read_html_conf(csv_path)
    js = json.dumps(csv, indent=2).strip()
    with open(json_path, "w+") as f:
        f.write(js)

if __name__ == "__main__":
    csv_path = "cnf/htmltagsdip.csv"
    json_path = "cnf/test0.json"
    do_main(csv_path, json_path)
