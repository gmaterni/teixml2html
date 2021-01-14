#!/usr/bin/env python
# coding: utf-8

s = """

teixml2html.py
    trasforma file xm in file html utilizzando un fil di
    csv dve sono definiti le entity per l trasformazione

librerie:
    htmlbuilder.py
        costruisce nodo per nodo un file HTML

    htmloverflow.py
         gestisce gli overflow tei DEI FILE XML:
         discorso diretto, monologo, parole danneggiate
    
    readhtmlconf.py
        legge il file dele enntitiy htmltag.csv e tarsgorma
        i dati in un dictionary

    readjson.py
        legge i file json e restitusice un dictionary

writehtmlfile.py
    copia un  file template html all'interno di un progetto
    gestitpo da prjmgr.py

writehtml.py
    copia un template html all'interno di un progetto
    gestitpo da prjmgr.py

copy2all.py
  copia i file json di un manoscritto in quelli di n 
  manoscriiti

htmlformat.py
    formatta i file htmlformat
    
prjmgr.py
    gestisce progetti definiti in file json

splitteixml.py
  separa iun file xml di un manoscritto nei file xml dei
  vari capitoli/eoisodi

uainput.py
    utiliti per il debug di teimed3html

ualog.py
    gestione dei log

"""


def list_modules():
    print(s)
    print("")


list_modules()
