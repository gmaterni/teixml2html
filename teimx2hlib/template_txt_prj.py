#!/usr/bin/env python3
# -*- coding: utf-8 -*-


__date__ = "30-03-2021"
__version__ = "0.1.0"
__author__ = "Marta Materni"

prj = {
    "witness": {
        "exe": [
            "prjmgr.py prj/witness_xml.json",
            "prjmgr.py prj/witness_txt.json",
        ]
    },

    "witness_xml": {
        "log": "0",
        "exe": [
            [
                "splitteixml.py",
                "-i xml/witness.xml",
                "-o xml/witness/",
                "-m witness"
            ]
        ]
    },

    "witness_txt": {
        "log":"0",
        "exe_dir": {
            "dir": "xml/witness",
            "pattern": "*.xml",
            "par_subst": ".xml|",
            "par_name": "$F",
            "exe_file": [
                [
                    "teixml2txt.py",
                    "-i xml/witness/$F.xml",
                    "-o txt/witness/txt/$F.txt",
                    "-c prj_cfg/witness_inter_txt.json",
                    "-wa w "
                ]
            ]
        }
    },


    "witness_rtemove_log": {
        "log": "1",
        "remove_dir": [
            {
                "dir": "xml/witness",
                "pattern": "*.*"
            },
            {
                "dir": "log",
                "pattern": "*.*"
            },
            {
                "dir": "txt/witness/txt",
                "pattern": "witness_list.txt"
            }
        ]
    }

}


prj_cfg = {

    "list_inter_txt": {
        "txt_params": {
            "text_null": "",
            "<null>": "",
            "</null>": ""
        },
        "txt_tag_file": "cfg/txt.csv",
        "before_id": "i"
    },

    "witness_inter_txt": {
        "txt_params": {
            "text_null": "",
            "_QA_": "\"",
            "_QC_": "\""
        },
        "txt_tag_file": "cfg/txt.csv",
        "txt_tag_type": "i:txt",
        "before_id": "i"
    }
}
