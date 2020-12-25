#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re

s="""
<div id="MAN_dip_id" class="text_pannel tei_dip">
    INCLUDE
</div>
<div id="MAN_int_id" class="text_pannel tei_int">
    INCLUDE
</div>
"""

def f(e):
    sp=e.split('INCLUDE')
    for i,x in enumerate(sp):
        print(i,x.strip())

f(s)


    

