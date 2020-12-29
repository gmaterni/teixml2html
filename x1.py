#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re

text="""
   p0 (/) %/%  
   p1 %par1% 
   p2 %par2%  
   p3(.) %.% 
   p4(;) %;%  
   p5(:) %:%  
   p6(^) %^% 
   p7(p-x)  %p-x%
   p8(p_y) %p_y% 
   p9(_)  %_%   
   p10(,) %,%  
   p11(?) %?% 
   p12(!) %!%
   p13 (^) %^%
   <div class="" cb_tt>%pb_n%%n%</div></div>
"""

def fn(ptrn):
    lst=re.findall(ptrn,text)
    s=text
    for i,x in enumerate(lst):
        print(i,x)
        s=s.replace(x,f'A_{i}_')
    print(s)

# ptrn=r"%[\S]%"
ptrn=r"%[\w/,;:.?!^-]+%"
fn(ptrn)
