files per l'esecuzione nella dir
prjmgr.py prj/<file>.json
----------------------------------
esecuzione  le fasi del projetto
(per semplicità tutti gli scritti fanno riferimento
al manoscritto pcon sigla ar)
----------------------------------
par_xml.json

{
    "exe": [
        [
            "splitteixml.py",
            "-i xml/floripar.xml",
            "-o xml/par/",
            "-m par"
        ]
    ]
}


---------------------------------
par_txt.json

{
  "exe_dir": {
    "dir": "xml/par",
    "pattern": "*.xml",
    "par_subst": ".xml|",
    "par_name": "$F",
    "exe_file": [
      [
        "teixml2html.py",
        "-i xml/par/$F.xml",
        "-o html/par/txt/$F.html",
        "-c cnf/par_dipl_txt.json",
        "-wa w"
      ],
      [
        "writehtml.py ",
        "-o html/par/txt/$F.html",
        "-wa a"
      ],
      [
        "teixml2html.py",
        "-i xml/par/$F.xml",
        "-o html/par/txt/$F.html",
        "-c cnf/par_inter_txt.json",
        "-wa a"
      ]
    ]
  },
  "remove_dir": [
    {
      "dir": "html/par/txt",
      "pattern": "par_list.html"
    }
  ]
}


-----------------------------------------
par_txt_pannel.json_path

{
  "exe": [
    [
      "writehtml.py",
      "-o html/par/txt/par.html",
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
      "-i xml/par/par_list.xml",
      "-o html/par/txt/par.html",
      "-c cnf/list_dipl_txt.json",
      "-wa a"
    ],
    [
      "writehtml.py",
      "-o html/par/txt/par.html",
      "-i '</div>",
      "<div id=\"pannel_int_id\" class=\"text_pannel\">",
      "<div id=\"notes_int_id\" class=\"notes\"></div>'",
      "-wa a"
    ],
    [
      "teixml2html.py",
      "-i xml/par/par_list.xml",
      "-o html/par/txt/par.html",
      "-c cnf/list_inter_txt.json",
      "-wa a"
    ],
    [
      "writehtml.py",
      "-o html/par/txt/par.html",
      "-i '</div></div>'",
      "-wa a"
    ]
  ]
}


--------------------------------
par.json

{
    "exe": [
        "prjmgr.py prj/par_xml.json",
        "prjmgr.py prj/par_syn.json",
        "prjmgr.py prj/par_syn_pannel.json",
        "prjmgr.py prj/par_txt.json",
        "prjmgr.py prj/par_txt_pannel.json"
    ]
}

--------------------------------
project.json

{
    "exe": [
        "prjmgr.py prj/par.json",
        "prjmgr.py prj/tor.json",
        "prjmgr.py prj/tou.json",
        "prjmgr.py prj/ven.json"
    ]
}


-------------------------------


