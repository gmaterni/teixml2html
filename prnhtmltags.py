#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
COL_NUM=7
BLK='                                                                                            '


def format_csv(rows):
    lsb=['','','','','','','']
    row_lst=[]
    for row in rows:
        if row.strip()=="":
            continue
        row= row.replace(os.linesep,'')
        flds = row.split('|')
        le=len(flds)
        if  le < COL_NUM:
            flds.extend(lsb[0:COL_NUM-le])
        row_lst.append(flds)
    lswd=[0 for x in range(0,COL_NUM) ]
    for row in row_lst:
        for i,f in enumerate(row):
            le=len(f.strip())
            lswd[i]=max(lswd[i],le)
    rows=[]
    for row in row_lst:
        ls=[]
        for i,f in enumerate(row):
            f=f.strip()
            b=BLK[0:lswd[i]-len(f)]
            lm=min(lswd[i],30)
            s=f'{f}{b}'[0:lm]
            ls.append(s)
        s="|".join(ls)
        rows.append(s)
    return rows
    

def read_csv_tags(csv_path):
    with open(csv_path, "r+") as f:
        rows = f.readlines()
    csv=format_csv(rows)
    for row in csv:
        print(row)


if __name__ == "__main__":
    tags_path = sys.argv[1]
    read_csv_tags(tags_path)
