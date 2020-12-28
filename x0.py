#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def t_split(s):
    sp = s.split(':')
    s0 = sp[0]
    le = len(sp)
    if le > 1:
        s1 = sp[1]
    else:
        s1 = ''
    return s0, s1


"""
        
        d   i   xt  xs  dt  ds  it  is
    x   1   1   1   1   1   1   1   1
    
    d   1   0   1   1   1   1   0   0
    i   0   1   1   1   0   0   1   1
    
    xt  0   0   1   0   1   0   1   0
    xs  0   0   0   1   0   1   0   1
    
    dt  0   0   1   0   1   0   0   0
    ds  0   0   0   1   0   1   0   0

    it  0   0   1   0   0   0   1   0
    is  0   0   0   1   0   0   0   1
    
    """


def row_ok(t, e):
    if t == 'x' or t == e:
        return True
    e0, e1 = t_split(e)
    if t.find(':') < 0:
        if t == e0 or e0 == 'x':
            return True
    else:
        t0, t1 = t_split(t)
        if t0 == 'x' and t1 == e1:
            return True
        if e0 == 'x' and t1 == e1:
            return True
    return False


def xbuild_list():
    l1 = ['x', 'd', 'i']
    l2 = ['t', 's']
    lst = []
    for a in l1:
        for b in l1:
            lst.append([a, b])
        for x in l2:
            lst.append([a, a+':'+x])
            lst.append([a+':'+x, a])
    return lst

def build_list():
    l1 = ['x', 'd', 'i']
    l2= ['x:t','x:s','d:t','d:s','i:t','i:s']
    for a in l1:
        for b in l1:
            r=row_ok(a,b)
            print(a,b,r)
    for a in l1:
        for x in l2:
            r=row_ok(a,x)
            print(a,x,r)

    for x in l2:
        for y in l2:
            r=row_ok(x,y)
            print(x,y,r)
    for x in l2:
        for a in l1:
            r=row_ok(x,a)
            print(x,a,r)




build_list()
