

{
  "html_params": {
    "text_null": "",
    "<null>": "",
    "</null>": ""
  },
  "html_info": "cnf/html.csv",
  "html_type":"d",
  "before_id":"d"
}

html_params
    utilizza i parametri nei files html dopo la 
    trasformazione da xml.
    il termine di sinnstra e la key quello di 
    destra il valore da sosituire    
        "text_nul""  => ""
        "<null>"    =>  "",
        "</null>"    =>  ""
html_info
    file di configurazione csv per le entity html
    es. cnf/html.csv"

html_type
    d = >  diplomatica
    i =>   interpretativa

before_id
    prefisso utilizzato per distinguere gli id
    dei file della diplmatica da quelli dell'interpretativa
    
========================================
file delle entity htm

type|xml_tag|tag|keys|attrs|text|params|parent

type selettore della tipologia
  x   per tutti i tipi
  d   diplomatica
  i   interpretativa
  x:txt txt per diplomatica ed interpretativa
  x:syn syn per diplomatica ed interpretativa
  d:txt txt per diplomatica 
  i:txt txt per interpretativa
  d:syn syn per diplomatica 
  i:syn syn per interpretativa

xml_tag
  tag xml per la selezione della riga csv2json

tag
  tag HTML 

keys
  elemco keys degli degli attributi di xml d
  a utilizzare nella trasformazione

attrs
  attributi da aggiungere in HTMLF

text
  testo da aggiungere in HTML

params
  parametri nella forma key9,val', key1:val1, ..
  da utilizzare per settare attrs e il text di xml

parent
  utilizza il settore xml del pade quando serve  uainput
  riferimento ad esso nella peoduzione HTML

====================================
testoisul quale si eseguono le sostituzioni
i parametri nel testo sono indicati con il pattern
%param%

  html_attrs
    attributi di xml selezionati da csv.c_key + csv.attrs

parametri
 text    
    tsto XML
  params
    params di csv
  items
    attributi di XML

sequenza sosituzioni:
  parametro     testo

  text         html_attrs
  params       ... (modificto dala recednete sostituzione) 
  items        ... (modificato dalla precebdente sostituzione)

---------------------------

text
  testo aggiuntivo definito in csv

ext_items
  parametri che uniscono
    xml pranet items (attributi del parente xml se definito in csv)
    xml items (attributi del nodo xml)
    csv attrs (attributi definiti in csv)
    %text% testo definito in xml

sequenza sosituzioni:
  parametro     testo
  
  ezx_items     text
  text          ...
  params        ''' 

====================================

esempi.

tag  per il controllo degli erroi  nei tag non trovati

x|x|_x_
x|x+y|_xy_

