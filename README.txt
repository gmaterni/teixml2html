file Nche NON sono sotto il controllo git
tutti le indiczioni sono riferite al manoscritto par
ma sono da cosiderarsi equivalenti per
tor,tou,ven sostituendo ila sigla adel manoscritto a par

bin
dir dei comandi di lavoro

html
html/par/txt
html/par/syn
......
output dei file html

htmlf
htmlf/par/txt
htmlf/par/syn
......
output dei file html formattati per il debug

log
dir dei log

==================================
Files soot controllo git

xml
xml/floripar.xml
......
files xml dei vari manoscritti

xml/par
......
dir contenete i files degli episodi

cnf
dir dei files di configurazione

prj
dir dei files di prohetto
=============================

file di configurzione:

html.csv
 entity per la produzione di htmlf/par/

list_dipl_syn.json
list_dipl_txt.json
list_inter_syn.json
list_inter_txt.json
    file per la produzione dei pannelli di gestione

par_dipl_syn.json
par_dipl_txt.json
par_inter_syn.json
par_inter_txt.json
    produzione dei files html delle sezioni

tidy.cnf
    file di configurazione di tidy poer la formattazione dei
    file htmlf
================================
file per esecuzione deile varie fasi

par_xml.json
    produce i files xml degli episodi
    xml/floripar.xml => xml/par/epi<num<.xml
    utilizza:
        prj/par_xml.json

par_txt.json
    files xml per txt
    xml/par/*.xml => html/par/txt/eps<num>.html
    utilizza:
        par_dipl_txt.json
        par_inter_txt.json

par_txt_pannel.json
    file per il pannello txt
    xml/par/par_list.xml => html/par/txt/par.html
    utilizza:
        list_dipl_txt.json
        list_inter_txt.json

par_txt_format.json
    formatta i files html e rova eventuali errir
    html/par/txt/eps<num>.html => htmlf/par/txt/eps<num>_F.html

par_syn.json
par_syn_pannel.json
par_syn_format.json
    sstesse operazioni per par_syn_format

par.json
    esegute tutti i progetti json tranne format
        par_xml.json
        par_tx.json
        par_txt_pannel.json
        par_syn.json
        par_syn_pannel.json

project.json
    esegue
    par.json
    tor.json
    tou.json
    ven.json
=============================
programmi che esguono le trasformazione

prjmgr.py
    esegue tutte le operazioni del projetto.json
    es.
    prjmgr.py prj/project.json

splitteixml.py
    estraee dla file xml del manoscritto i files xmlm
    xml/floripar.xml => xml/par/eps<num>.xml

teixml2html.py
    trasforma xml in html
    xml/par/eps<num>.xml => html/par/txt/eps<num>.html

writehtmlfile.py
    lege un file html e lo scrive  all'intyerno dei progetti

writehtml.py
    scrive pezzi di html all'inerno di un progetto

htmlformat.py
    formatta i file html  e gli eventuali errori
    html/par/txt/eps<num>.html => htmlf/par/txt/eps<num>_F.html

copy_par2all.py
    copya file di configurazione e di progetto di par
    in tor, tou e ven

libreire
utilizzate da teixml2html.py

csv2json.py
    trasforma un csv in json

htmlbuilder.py
    costruisce la struttura htmlf/par/

htmloverflow.py
    gestisce overflow (discorso diretto, ..)

readhtmlconf.py
    legge i file csv

readjson.py
    legge i file json

uainput.py
    geisce il debug  mediante  input di controllo

ualog.py
    gestisce i log di tutte le applicazioni
