

{
  "html_params": {
    "text_null": "",
    "<null>": "",
    "</null>": ""
  },
  "html_tag_file": "cfg/html.csv",
  "html_tag_type":"d",
  "before_id":"d"
}

html_params
    utilizza i par1ametri nei files html dopo la
    trasformazione da xml.
    il termine di sinnstra e la key quello di
    destra il valore da sosituire
        "text_nul""  => ""
        "<null>"    =>  "",
        "</null>"    =>  ""
html_tag_file
    file di configurazione csv per le entity html
    es. cfg/html.csv"

html_tag_type
    d = >  diplomatica
    i =>   interpretativa

before_id
    prefisso utilizzato per distinguere gli id
    dei file della diplmatica da quelli dell'interpretativa

========================================
file delle entity htm

type|xml_tag|tag|keys|attrs|text|par1ams|par1ent

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

par1ams
  par1ametri nella forma key9,val', key1:val1, ..
  da utilizzare per settare attrs e il text di xml

par1ent
  utilizza il settore xml del pade quando serve  uainput
  riferimento ad esso nella peoduzione HTML

-----------------
type|tag|XXX

rimuove il tag

====================================
testo sul quale si eseguono le sostituzioni
i par1ametri nel testo sono indicati con il pattern
%par1am%

  html_attrs
    attributi di xml selezionati da csv.c_key + csv.attrs

par1ametri
 text
    tsto XML
  par1ams
    par1ams di csv
  items
    attributi di XML

sequenza sosituzioni:
  par1ametro     testo

  text         html_attrs
  par1ams       ... (modificto dala recednete sostituzione)
  items        ... (modificato dalla precebdente sostituzione)

---------------------------

text
  testo aggiuntivo definito in csv

ext_items
  par1ametri che uniscono
    xml pranet items (attributi del par1ente xml se definito in csv
                      le coppye k,v hanno la forma tag_k,v dove tag è
                      quella del parent)
    xml items (attributi del nodo xml)
    csv attrs (attributi definiti in csv)
    %text% testo definito in xml

sequenza sosituzioni:
  par1ametro     testo

  ezx_items     text
  text          ...
  par1ams        '''

====================================
esempi.

tag  per il controllo degli erroi  nei tag non trovati

x|x|_x_
x|x+y|_xy_
====================================
<placeName>
contiene sempre <name> (da mettere in maiuscolo)
ed ha l'attributo @type
nel mio caso è stato specificato type="region", type="city", type="castel"
ma il valore dell'attributo non influisce sul comportamento delle maiuscole

caso tipo
<placeName type="region" ref="#$">
     <name><w>$</w></name>
</placeName>

<geogName>
contiene sempre <name> (da mettere in maiuscolo)
può contenere <geogFeat> (NON va in maiuscolo)
può avere l'attributo @type, finora non l'ho usato ma è abbastanza comune che ci sia, quindi va previsto. come nel caso di placeName comunque il valore dell'attributo non influisce sul trattamento delle maiuscole

casi tipo
<geogName ref="#$">
    <name><w>$</w></name>
</geogName>

<geogName ref="#$">
     <geogFeat><w>$</w></geogFeat>
     <w>$</w>
    <name><w>$</w></name>
</geogName>

