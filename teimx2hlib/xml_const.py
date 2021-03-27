#!/usr/bin/env python3
# -*- coding: utf-8 -*-


__date__ = "16-01-2021"
__version__ = "0.1.0"
__author__ = "Marta Materni"


XML_DECL = "<?xml version='1.0' encoding='utf-8' standalone='yes'?>"
TEI_TOP="<TEI>"
TEI_BOTTOM = "</TEI>"

BODY_TOP="<body>"
BODY_TOP_PATTERN=r"<\s*body\s*>"
BODY_BOTTOM_PATTERN = r"</\s*body\s*>"
BODY_BOTTOM = "</body>"

BACK_TOP = "<back>"
BACK_BOTTOM = "</back>"

NOTE_TOP = '<div type="note">'
NOTE_BOTTOM = "</div>"

NULL_TAG_START="<null>"
NULL_TAG_END="</null>"
 
"""
tostring(element_or_tree, 
encoding=None, 
method="xml", 
xml_declaration=None, 
pretty_print=False, 
with_tail=True, 
standalone=None, 
doctype=None, 
exclusive=False, 
inclusive_ns_prefixes=None, 
with_comments=True, 
strip_text=False
 )
"""
 

