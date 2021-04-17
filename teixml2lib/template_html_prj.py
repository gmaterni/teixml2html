#!/usr/bin/env python3
# -*- coding: utf-8 -*-


__date__ = "22-01-2021"
__version__ = "0.1.0"
__author__ = "Marta Materni"

prj = {
    "witness": {
        "exe": [
            "prjmgr.py prj/witness_xml.json",
            "prjmgr.py prj/witness_syn.json",
            "prjmgr.py prj/witness_syn_pannel.json",
            "prjmgr.py prj/witness_txt.json",
            "prjmgr.py prj/witness_txt_pannel.json"
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

    "witness_syn": {
        "log": "0",
        "exe_dir": {
            "dir": "xml/witness",
            "pattern": "*.xml",
            "par_subst": ".xml|",
            "par_name": "$F",
            "exe_file": [
                [
                    "writehtml.py",
                    "-o html/witness/syn/$F.html",
                    "-i '<div id=\"witness_dipl_id\" class=\"text_pannel tei_dipl\">'",
                    "-wa w"
                ],
                [
                    "teixml2html.py",
                    "-i xml/witness/$F.xml",
                    "-o html/witness/syn/$F.html",
                    "-c prj_cfg/witness_dipl_syn.json",
                    "-wa a "
                ],
                [
                    "writehtml.py",
                    "-o html/witness/syn/$F.html",
                    "-i '</div><div id=\"witness_int_id\" class=\"text_pannel tei_int\">'",
                    "-wa a"
                ],
                [
                    "teixml2html.py",
                    "-i xml/witness/$F.xml",
                    "-o html/witness/syn/$F.html",
                    "-c prj_cfg/witness_inter_syn.json",
                    "-wa a "
                ],
                [
                    "writehtml.py",
                    "-o html/witness/syn/$F.html",
                    "-i '</div>'",
                    "-wa a"
                ]
            ]
        }
    },

    "witness_syn_pannel": {
        "log": "0",
        "exe": [
            [
                "writehtml.py",
                "-o html/witness/syn/witness.html",
                "-i '<div id=\"witness_dip_id\" class=\"text_pannel tei_dip\">'",
                "-wa w"
            ],
            [
                "teixml2html.py",
                "-i xml/witness/witness_list.xml",
                "-o html/witness/syn/witness.html",
                "-c prj_cfg/list_dipl_syn.json",
                "-wa a"
            ],
            [
                "writehtml.py",
                "-o html/witness/syn/witness.html",
                "-i '</div>",
                "<div id=\"witness_int_id\" class=\"text_pannel tei_int\">'",
                "-wa a"
            ],
            [
                "teixml2html.py",
                "-i xml/witness/witness_list.xml",
                "-o html/witness/syn/witness.html",
                "-c prj_cfg/list_inter_syn.json",
                "-wa a"
            ],
            [
                "writehtml.py",
                "-o html/witness/syn/witness.html",
                "-i '</div>'",
                "-wa a"
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
                    "teixml2html.py",
                    "-i xml/witness/$F.xml",
                    "-o html/witness/txt/$F.html",
                    "-c prj_cfg/witness_dipl_txt.json",
                    "-wa w "
                ],
                [
                    "writehtml.py ",
                    "-o html/witness/txt/$F.html",
                    "-wa a"
                ],
                [
                    "teixml2html.py",
                    "-i xml/witness/$F.xml",
                    "-o html/witness/txt/$F.html",
                    "-c prj_cfg/witness_inter_txt.json",
                    "-wa a "
                ]
            ]
        }
    },


    "witness_txt_pannel": {
        "log": "0",
        "exe": [
            [
                "writehtml.py",
                "-o html/witness/txt/witness.html",
                "-i '<div id=\"eps_id\"></div>",
                "<div id=\"teimed_id\">",
                "<div id=\"bar_text_id\"></div>",
                "<div id=\"bar_img_id\"></div>",
                "<div id=\"barv_text_id\"></div>",
                "<div id=\"teimed_help_id\"></div>",
                "<div id=\"teimed_bar_id\"></div>",
                "<div id=\"teimed_abr_id\"></div>",
                "<div id=\"pannel_img_id\" class=\"img\"></div>",
                "<div id=\"pannel_dip_id\" class=\"text_pannel\">",
                "<div id=\"notes_dip_id\" class=\"notes\"></div>'",
                "-wa w"
            ],
            [
                "teixml2html.py",
                "-i xml/witness/witness_list.xml",
                "-o html/witness/txt/witness.html",
                "-c prj_cfg/list_dipl_txt.json",
                "-wa a"
            ],
            [
                "writehtml.py",
                "-o html/witness/txt/witness.html",
                "-i '</div>",
                "<div id=\"pannel_int_id\" class=\"text_pannel\">",
                "<div id=\"notes_int_id\" class=\"notes\"></div>'",
                "-wa a"
            ],
            [
                "teixml2html.py",
                "-i xml/witness/witness_list.xml",
                "-o html/witness/txt/witness.html",
                "-c prj_cfg/list_inter_txt.json",
                "-wa a"
            ],
            [
                "writehtml.py",
                "-o html/witness/txt/witness.html",
                "-i '</div></div>'",
                "-wa a"
            ]
        ]
    },

    "witness_remove_log": {
        "log": "0",
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
                "dir": "html/witness/txt",
                "pattern": "witness_list.html"
            },
            {
                "dir": "html/witness/syn",
                "pattern": "witness_list.html"
            }
        ]
    }

}

###############################

prj_cfg = {

    "list_dipl_syn":    {
        "html_params": {
            "text_null": "",
            "<null>": "",
            "</null>": ""
        },
        "html_tag_file": "cfg/html.csv",
        "html_tag_type": "d:syn",
        "dipl_inter": "d",
        "before_id": "d"
    },

    "list_dipl_txt": {
        "html_params": {
            "text_null": "",
            "<null>": "",
            "</null>": ""
        },
        "html_tag_file": "cfg/html.csv",
        "html_tag_type": "d",
        "dipl_inter": "d",
        "before_id": "d"
    },

    "list_inter_syn": {
        "html_params": {
            "text_null": "",
            "<null>": "",
            "</null>": ""
        },
        "html_tag_file": "cfg/html.csv",
        "html_tag_type": "i:syn",
        "dipl_inter": "i",
        "before_id": "i"
    },

    "list_inter_txt": {
        "html_params": {
            "text_null": "",
            "<null>": "",
            "</null>": ""
        },
        "html_tag_file": "cfg/html.csv",
        "html_tag_type": "i",
        "dipl_inter": "i",
        "before_id": "i"
    },

    "witness_dipl_syn": {
        "html_params": {
            "_MAN_": "witness",
            "text_null": "",
            "_QA_": "\"",
            "_QC_": "\""
        },
        "html_tag_file":  "cfg/html.csv",
        "html_tag_type": "d:syn",
        "dipl_inter": "d",
        "before_id": "d"
    },

    "witness_dipl_txt": {
        "html_params": {
            "_MAN_": "witness",
            "text_null": "",
            "_QA_": "\"",
            "_QC_": "\""
        },
        "html_tag_file": "cfg/html.csv",
        "html_tag_type": "d:txt",
        "dipl_inter": "d",
        "before_id": "d"
    },

    "witness_inter_syn": {
        "html_params": {
            "text_null": "",
            "_QA_": "\"",
            "_QC_": "\""
        },
        "html_tag_file":  "cfg/html.csv",
        "html_tag_type": "i:syn",
        "dipl_inter": "i",
        "before_id": "i"
    },

    "witness_inter_txt": {
        "html_params": {
            "text_null": "",
            "_QA_": "\"",
            "_QC_": "\""
        },
        "html_tag_file": "cfg/html.csv",
        "html_tag_type": "i:txt",
        "dipl_inter": "i",
        "before_id": "i"
    }

}
