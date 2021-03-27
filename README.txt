file che NON sono sotto il controllo git
tutti le indiczioni sono riferite al manoscritto par1
ma sono da cosiderarsi equivalenti per
tor,tou,ven sostituendo ila sigla adel manoscritto a par1

bin
dir dei comandi di lavoro

html
html/par1/txt
html/par1/syn
......
output dei file html

htmlf
htmlf/par1/txt
htmlf/par1/syn
......
output dei file html formattati per il debug

log
dir dei log

==================================
Files soot controllo git

xml
xml/floripar1.xml
......
files xml dei vari manoscritti

xml/par1
......
dir contenete i files degli episodi

cnf
dir dei files di configurazione

prj
dir dei files di prohetto
=============================

file di configurzione:

html.csv
 entity per la produzione di htmlf/par1/

list_dipl_syn.json
list_dipl_txt.json
list_inter_syn.json
list_inter_txt.json
    file per la produzione dei pannelli di gestione

par1_dipl_syn.json
par1_dipl_txt.json
par1_inter_syn.json
par1_inter_txt.json
    produzione dei files html delle sezioni

tidy.cnf
    file di configurazione di tidy poer la formattazione dei
    file htmlf
================================
file per esecuzione deile varie fasi

par1_xml.json
    produce i files xml degli episodi
    xml/floripar1.xml => xml/par1/epi<num<.xml
    utilizza:
        prj/par1_xml.json

par1_txt.json
    files xml per txt
    xml/par1/*.xml => html/par1/txt/eps<num>.html
    utilizza:
        par1_dipl_txt.json
        par1_inter_txt.json

par1_txt_pannel.json
    file per il pannello txt
    xml/par1/par1_list.xml => html/par1/txt/par1.html
    utilizza:
        list_dipl_txt.json
        list_inter_txt.json

par1_txt_format.json
    formatta i files html e rova eventuali errir
    html/par1/txt/eps<num>.html => htmlf/par1/txt/eps<num>_F.html

par1_syn.json
par1_syn_pannel.json
par1_syn_format.json
    sstesse operazioni per par1_syn_format

par1.json
    esegute tutti i progetti json tranne format
        par1_xml.json
        par1_tx.json
        par1_txt_pannel.json
        par1_syn.json
        par1_syn_pannel.json

project.json
    esegue
    par1.json
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
    xml/floripar1.xml => xml/par1/eps<num>.xml

teixml2html.py
    trasforma xml in html
    xml/par1/eps<num>.xml => html/par1/txt/eps<num>.html

writehtmlfile.py
    lege un file html e lo scrive  all'intyerno dei progetti

writehtml.py
    scrive pezzi di html all'inerno di un progetto

htmlformat.py
    formatta i file html  e gli eventuali errori
    html/par1/txt/eps<num>.html => htmlf/par1/txt/eps<num>_F.html

copyxml.py
    copya file xml da un projetto xml ad un progetto html
     es. copyxml.py flori
        copia i files xml da flori_xml =>  flori_tml   

libreire
utilizzate da teixml2html.py

csv2json.py
    trasforma un csv in json

htmlbuilder.py
    costruisce la struttura htmlf/par1/

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
