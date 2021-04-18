ano=${1:-'x'}
source ./setflenv.sh
fl2eps.sh ${mano}
xtxtfl2h.sh ${mano}
xsynfl2h.sh ${mano}
=====================
fl2eps.sh ${mano}
----------------
 divide il file di un manoscritto in episodi
# floripar1.xml  =>
# par1.txt (elenco episodi)
# ep1.xml (episodio 1)
# ep2.xml (episodio 2)
sigla=${1}
fl2eps.py -i "xml/${sigla}/flori${sigla}.xml" -o "xml/${sigla}/${sigla}"
=====================
xtxtfl2h.sh ${mano}
nell'esempip ${mano} = par1
-------------------
# diplomatica
xml/par1/par1.xml => html/par1/txt/xdip.html
#interpretativa
xml/par1/par1.xml => html/par1/txt/xint.html
---------------------
# html con div di gestione

fl_divs.html                                   => html/par1/txt/par1.html
#
<div id="pannel_dip_id" class="text_pannel ">  =>> html/par1/txt/par1.html
<div id="notes_dip_id" class="notes"></div>    =>> html/par1/txt/par1.html
html/par1/txt/xdip.html                         =>> html/par1/txt/par1.html
</div>                                         =>> html/par1/txt/par1.html
#
<div id="pannel_int_id" class="text_pannel "> =>> html/par1/txt/par1.html
<div id="notes_int_id" class="notes"></div>'  =>> html/par1/txt/par1.html
html/par1/txt/xint.html                        =>> html/par1/txt/par1.html
</div>                                        =>> html/par1/txt/par1.html
#
</div>                                        =>> html/par1/txt/par1.html
=================================
# legge elenco episori i par1.txt per ognuno
# lancia xtxtep2h.sh ep<n>  par1
=================================
# diplomatica
xml/par1/ep<n>.xml => html/par1/txt/xdip.html
# interpretativa
xml/par1/ep<n>.xml => html/par1/txt/xint.html
----------------------
# unisce in una file diplomatica ed interpreattiva
html/par1/txt/xdip.html =>  html/par1/txt/ep<n>.html
html/par1/txt/xint.html =>> html/par1/txt/ep<n>.html
******************************************************
SYN
******************************************************
xsynfl2h.sh ${mano}
nell'esempip ${mano} = par1
------------
# diplomatica
xml/par1/par1.xml => html/par1/syn/xdip.html
# interpretativa
xml/par1/par1.xml => html/par1/syn/xint.html
--------------------
"" => html/par1/syn/par1.html
html/par1/syn/xdip.html =>> html/par1/syn/par1.html
html/par1/syn/xdip.html =>> html/par1/syn/par1.html
=================================
# legge elenco episori i par1.txt per ognuno
# lancia xsynep2h.sh ep<n>  par1
=================================
# diplomatica
xml/par1/ep<n>.xml => html/par1/syn/xdip.html
# interpretativa
xml/par1/ep<n>.xml => html/par1/syn/xint.html
-----------------------
# unisce diplomatica ed interpretativa
html/par1/syn/xdip.html => html/par1/syn/ep<n>.html
html/par1/syn/xdinthtml =>> html/par1/syn/ep<n>.html






































