************************************TIE2*************************************
**************************David Ricardo y Yuri Solari*************************
***Obtener ingreso por distrito

***Base de cantidad en cada distrito
clear
cd "C:\Users\dipa_\OneDrive - UDEP\UDEP\2023\TIE\Final"
import excel cantidades.xlsx, firstrow
rename AÑO year
rename MES month
rename Distrito distrito
replace month="1" if month=="ENERO"
replace month="2" if month=="FEBRERO"
replace month="3" if month=="MARZO"
replace month="4" if month=="ABRIL"
replace month="5" if month=="MAYO"
replace month="6" if month=="JUNIO"
replace month="7" if month=="JULIO"
replace month="8" if month=="AGOSTO"
replace month="9" if month=="SEPTIEMBRE"
replace month="10" if month=="OCTUBRE"
replace month="11" if month=="NOVIEMBRE"
replace month="12" if month=="DICIEMBRE"
drop GLPAutomotriz
reshape long Gasohol, i(year month distrito) j(producto)
rename Gasohol cantidad
gen primera=substr(distrito,1,3)
replace distrito="BRENA" if primera=="BRE"
replace distrito="MAGDALENA" if primera=="MAG"
replace month="5" if month=="MAYO "
destring producto, replace
destring month, replace
keep if producto==90 | producto==95 
drop primera
drop if distrito=="ASIA" | distrito=="AUCALLAMA" | distrito=="BARRANCA" | distrito=="CANTA" | distrito=="CERRO AZUL" | distrito=="AUCALLAMA" | distrito=="CHANCAY" | distrito=="CHILCA" | distrito=="CUENCA" | distrito=="HUACHO" | distrito=="HUALMAY" | distrito=="HUARAL" | distrito=="HUAURA" | distrito=="IMPERIAL" | distrito=="LUNAHUANA" | distrito=="MALA" | distrito=="MATUCANA" | distrito=="NUEVO IMPERIAL" | distrito=="OYON" | distrito=="PARAMONGA" | distrito=="PATIVILCA" | distrito=="QUILMANA" | distrito=="RICARDO PALMA" | distrito=="SAN ANTONIO" | distrito=="SAN MATEO" | distrito=="SAN VICENTE DE CAÑETE" | distrito=="SANTA CRUZ DE COCACHACRA" | distrito=="SANTA EULALIA" | distrito=="SANTA MARIA" | distrito=="SANTA ROSA DE QUIVES" | distrito=="SANTO DOMINGO DE LOS OLLEROS" | distrito=="SAYAN" | distrito=="SUPE" | distrito=="VEGUETA" | distrito=="SUPE PUERTO" | distrito=="MI PERU"
drop if distrito=="Ml PERU"
drop if distrito=="PUNTA HERMOSA"
drop if distrito=="PUNTA NEGRA" /**/
drop if distrito=="SANTA MARIA DEL MAR"
drop if distrito=="CARMEN DE LA LEGUA REYNOSO" 
drop if year==2019
drop if year==2020 & month==1
drop if year==2020 & month==2
replace cantidad=0 if cantidad==. 
replace cantidad=1 if cantidad==0
save cantidades, replace

***Deflactor del petróleo nacional
clear
cd "C:\Users\dipa_\OneDrive - UDEP\UDEP\2023\TIE\Final"
import excel ipc2021.xlsx, firstrow
save ipcperu.dta, replace

***Deflactor del petróleo crudo
clear
cd "C:\Users\dipa_\OneDrive - UDEP\UDEP\2023\TIE\Final"
import excel cpi_eeuu.xlsx, firstrow
save ipcint.dta, replace

***Precios del petróleo crudo
clear
cd "C:\Users\dipa_\OneDrive - UDEP\UDEP\2023\TIE\Final"
import excel Brent.xlsx, firstrow
gen year = substr(Date,7,4) 
gen month = substr(Date,1,2) 
destring year, replace
destring month, replace
drop Date g90 g95

merge 1:1 year month using ipcint.dta
*drop if _merge==1
drop _merge  

gen brent_def = (Brent/ipcint)*100
drop Brent 
rename brent_def Brent

gen lag1 = Brent[_n-1]
gen lag2 = Brent[_n-2]
gen lag3 = Brent[_n-3]
gen lag4 = Brent[_n-4]
gen lag5 = Brent[_n-5]
gen lag6 = Brent[_n-6]
gen lag7 = Brent[_n-7]
gen lag8 = Brent[_n-8]
gen lag9 = Brent[_n-9]
gen lag10 = Brent[_n-10]
gen lag11 = Brent[_n-11]
gen lag12 = Brent[_n-12]

gen llag1=ln(lag1)
gen llag2=ln(lag2)
gen llag3=ln(lag3)
gen llag4=ln(lag4)
gen llag5=ln(lag5)
gen llag6=ln(lag6)
gen llag7=ln(lag7)
gen llag8=ln(lag8)
gen llag9=ln(lag9)
gen llag10=ln(lag10)
gen llag11=ln(lag11)
gen llag12=ln(lag12)


drop if year==2019
drop if year==2020 & month==1
drop if year==2020 & month==2

save Brent.dta, replace

***Cantidad de grifos en cada distrito
clear all
cd "C:\Users\dipa_\OneDrive - UDEP\UDEP\2023\TIE\Final"
use BD_grifos3.dta
rename COORDENADAS3 coordenadas
rename DISTRITO distrito
drop if distrito=="MI PERU"
drop if distrito=="Ml PERU"
drop if distrito=="PUNTA HERMOSA"
drop if distrito=="PUNTA NEGRA"
drop if distrito=="SANTA MARIA DEL MAR"
drop if distrito=="CARMEN DE LA LEGUA REYNOSO"
gen primera=substr(distrito,1,3)
replace distrito="BRENA" if primera=="BRE"
replace distrito="MAGDALENA" if primera=="MAG"
drop primera
keep distrito coordenadas
duplicates drop 
bysort distrito: gen a=_N
keep distrito a 
duplicates drop
save numgrif.dta, replace

***Base completa
clear all
cd "C:\Users\dipa_\OneDrive - UDEP\UDEP\2023\TIE\Final"
use BD_grifos3.dta

*1. Identificador de cada grifo

*2. Año
gen year = substr(MESA_O,1,4) 
destring, replace 

*3. Mes
gen month = substr(MESA_O,6,.) 

*4. Drop variables que no necesitamos
drop DEPARTAMENTO 
drop COORDENADAS3 

*5. Renombrar variables
rename MESA_O my
rename PRECIO_DE_VENTA__SOLES_ precio
rename DISTRITO distrito
rename PROVINCIA provincia
rename PRODUCTO producto
rename index id

*6. Creación de variables de coordenadas 

*7. Corrección de variables con errores
gen primera=substr(distrito,1,3)
replace distrito="BRENA" if primera=="BRE"
replace distrito="MAGDALENA" if primera=="MAG"
replace month="5" if month=="MAYO " 
drop primera

*8. Creación de variables instrumentales
egen mbuffer = mean(buffer2), by(distrito)

*9. Precio y precio deflactado  
destring month, replace
merge m:1 year month using ipcperu.dta 
drop if _merge==2
drop _merge 
gen pre_def=(precio/ipc_2021)*100
egen mpre_def = mean(pre_def), by(distrito year month producto)

*10. Reconfigurar variable de producto
replace producto="84" if producto=="GASOHOL 84 PLUS"
replace producto="90" if producto=="GASOHOL 90 PLUS"
replace producto="95" if producto=="GASOHOL 95 PLUS"
replace producto="97" if producto=="GASOHOL 97 PLUS"
replace producto="98" if producto=="GASOHOL 98 PLUS"
destring producto, replace 
keep if producto==90 | producto==95

*11. Base a nivel distrito
keep year month distrito producto mpre_def mbuffer 
duplicates drop 
save preliminar, replace 

*12. Añadir cantidad
destring month, replace
merge 1:1 year month distrito producto using cantidades.dta 
keep if _merge==3
drop _merge

*13. Limpieza
*Fuera de LMC
drop if distrito=="ASIA" | distrito=="AUCALLAMA" | distrito=="BARRANCA" | distrito=="CANTA" | distrito=="CERRO AZUL" | distrito=="AUCALLAMA" | distrito=="CHANCAY" | distrito=="CHILCA" | distrito=="CUENCA" | distrito=="HUACHO" | distrito=="HUALMAY" | distrito=="HUARAL" | distrito=="HUAURA" | distrito=="IMPERIAL" | distrito=="LUNAHUANA" | distrito=="MALA" | distrito=="MATUCANA" | distrito=="NUEVO IMPERIAL" | distrito=="OYON" | distrito=="PARAMONGA" | distrito=="PATIVILCA" | distrito=="QUILMANA" | distrito=="RICARDO PALMA" | distrito=="SAN ANTONIO" | distrito=="SAN MATEO" | distrito=="SAN VICENTE DE CAÑETE" | distrito=="SANTA CRUZ DE COCACHACRA" | distrito=="SANTA EULALIA" | distrito=="SANTA MARIA" | distrito=="SANTA ROSA DE QUIVES" | distrito=="SANTO DOMINGO DE LOS OLLEROS" | distrito=="SAYAN" | distrito=="SUPE" | distrito=="VEGUETA" | distrito=="SUPE PUERTO"  

*En LMC pero con muchos missings 
drop if distrito=="MI PERU"
drop if distrito=="Ml PERU"
drop if distrito=="PUNTA HERMOSA"
drop if distrito=="PUNTA NEGRA"
drop if distrito=="SANTA MARIA DEL MAR"
drop if distrito=="CARMEN DE LA LEGUA REYNOSO"

*Fuera del periodo observado
drop if year==2019
drop if year==2020 & month==1
drop if year==2020 & month==2

*14. Añadir Brent 
merge m:1 year month using Brent.dta
drop if year==2019
drop if year==2020 & month==1
drop if year==2020 & month==2
drop _merge

*15. Creación de variables logarítmicas
*Cantidad por grifo 
merge m:1 distrito using numgrif.dta 
drop _merge
replace cantidad=cantidad*30 if month==4 | month==6| month==9 | month==11
replace cantidad=cantidad*31 if month==1 | month==3 | month==5 | month==7 | month==8 | month==10 | month==12
replace cantidad=cantidad*28 if month==2
gen lprecio=ln(mpre_def)

keep year month distrito producto lprecio mbuffer llag* cantidad mpre_def  lag*
sort year month distrito producto 

*16. Añadir ingreso y predial

gen pobreza=.
replace pobreza=1456 if distrito =="ANCON"
replace pobreza=1523 if distrito =="ATE"
replace pobreza=1837 if distrito =="BARRANCO"
replace pobreza=1816 if distrito =="BELLAVISTA"
replace pobreza=1822 if distrito =="BRENA"
replace pobreza=1621 if distrito =="CALLAO"
replace pobreza=1459 if distrito =="CARABAYLLO"
replace pobreza=1735 if distrito =="CHACLACAYO"
replace pobreza=1691 if distrito =="CHORRILLOS"
replace pobreza=1518 if distrito =="CIENEGUILLA"
replace pobreza=1561 if distrito =="COMAS"
replace pobreza=1542 if distrito =="EL AGUSTINO"
replace pobreza=1413 if distrito =="INDEPENDENCIA"
replace pobreza=1870 if distrito =="JESUS MARIA"
replace pobreza=1864 if distrito =="LA MOLINA"
replace pobreza=1841 if distrito =="LA PERLA"
replace pobreza=1856 if distrito =="LA PUNTA"
replace pobreza=1705 if distrito =="LA VICTORIA"
replace pobreza=1761 if distrito =="LIMA"
replace pobreza=1860 if distrito =="LINCE"
replace pobreza=1762 if distrito =="LOS OLIVOS"
replace pobreza=1507 if distrito =="LURIGANCHO"
replace pobreza=1506 if distrito =="LURIN"
replace pobreza=1866 if distrito =="MAGDALENA"
replace pobreza=1873 if distrito =="MIRAFLORES"
replace pobreza=1432 if distrito =="PACHACAMAC"
replace pobreza=1310 if distrito =="PUCUSANA"
replace pobreza=1867 if distrito =="PUEBLO LIBRE"
replace pobreza=1358 if distrito =="PUENTE PIEDRA"
replace pobreza=1697 if distrito =="RIMAC"
replace pobreza=1646 if distrito =="SAN BARTOLO"
replace pobreza=1871 if distrito =="SAN BORJA"
replace pobreza=1874 if distrito =="SAN ISIDRO"
replace pobreza=1515 if distrito =="SAN JUAN DE LURIGANCHO"
replace pobreza=1577 if distrito =="SAN JUAN DE MIRAFLORES"
replace pobreza=1801 if distrito =="SAN LUIS"
replace pobreza=1725 if distrito =="SAN MARTIN DE PORRES"
replace pobreza=1858 if distrito =="SAN MIGUEL"
replace pobreza=1738 if distrito =="SANTA ANITA"
replace pobreza=1379 if distrito =="SANTA ROSA"
replace pobreza=1863 if distrito =="SANTIAGO DE SURCO"
replace pobreza=1847 if distrito =="SURQUILLO"
replace pobreza=1213 if distrito =="VENTANILLA"
replace pobreza=1421 if distrito =="VILLA EL SALVADOR"
replace pobreza=1540 if distrito =="VILLA MARIA DEL TRIUNFO"
gen lpobreza=ln(pobreza)
merge m:1 distrito using numgrif.dta
drop _merge
gen bartik=mbuffer*llag8
gen mcantidad=cantidad/(a)
gen lcantidad=ln(mcantidad)
save final, replace 

*17. Creación de bases separadas
keep if producto==90
save 90.dta, replace

clear
use final
keep if producto==95
save 95.dta, replace 

*18. Probar robustez (90) // Elegir instrumento // Correr regresión
clear
use 90 

*Elección final: llag2
*drop bartik 

save 90, replace

*OLS
reg lcantidad lprecio lpobreza, vce(ols)

*VI - B
ivregress 2sls lcantidad lpobreza (lprecio=bartik), first

*VI - B
ivregress 2sls lcantidad lpobreza (lprecio=mbuffer llag2), first 
*estat overid

*Reduced Form 
reg lcantidad lprecio lpobreza, vce(ols)

*19. Probar robustez (95) // Elegir instrumento // Correr regresión
clear
use 95 

*Elección final: llag3
*drop bartik 
save 95, replace

*OLS
reg lcantidad lprecio lpobreza, vce(ols)

*VI - B
ivregress 2sls lcantidad pobreza (lprecio=bartik), first

*VI - B
ivregress 2sls lcantidad lpobreza (lprecio=mbuffer llag2), first
*estat overid

*Reduced Form 
reg lcantidad lprecio lpobreza, vce(ols)

/*
*20. Probar heterogeneidad (90)
clear 
use 90
gen bartik=mbuffer*llag2
ivregress 2sls lcantidad lpobreza (lprecio=bartik), first

clear
use 90_ingresoalto
gen bartik=mbuffer*llag2
ivregress 2sls lcantidad lpobreza (lprecio=bartik), first

clear
use 90_ingresobajo
gen bartik=mbuffer*llag2
ivregress 2sls lcantidad lpobreza (lprecio=bartik), first

clear
use 90_sitransporte
gen bartik=mbuffer*llag2
ivregress 2sls lcantidad lpobreza (lprecio=bartik), first

clear
use 90_notransporte
gen bartik=mbuffer*llag2
ivregress 2sls lcantidad lpobreza (lprecio=bartik), first

clear
use 90_competitivo
gen bartik=mbuffer*llag2
ivregress 2sls lcantidad lpobreza (lprecio=bartik), first

clear
use 90_nocompetitivo
gen bartik=mbuffer*llag2
ivregress 2sls lcantidad lpobreza (lprecio=bartik), first

*21. Probar heterogeneidad (95)
/*
clear 
use 95
ivregress 2sls lcantidad lpobreza (lprecio=bartik), first

clear
use 95_ingresoalto
ivregress 2sls lcantidad lpobreza (lprecio=bartik), first

clear
use 95_ingresobajo
ivregress 2sls lcantidad lpobreza (lprecio=bartik), first

clear
use 95_sitransporte
ivregress 2sls lcantidad lpobreza (lprecio=bartik), first

clear
use 95_notransporte
ivregress 2sls lcantidad lpobreza (lprecio=bartik), first
*/
clear
use 95_competitivo
ivregress 2sls lcantidad lpobreza (lprecio=bartik), first

clear
use 95_nocompetitivo
ivregress 2sls lcantidad lpobreza (lprecio=bartik), first

************
*ivregress 2sls lcantidad (lprecio=lag2 mbuffer2)
*estat firststage 
*estat overid
*esttab, cells("mean") row(lprecio) column(lcantidad) label nonumber noobs booktabs
*/
gen rico = (pobreza >= 1705)
gen fecha = mdy(month, 1, year)
format fecha %tdMon-yy

collapse mcantidad, by(producto fecha)

	twoway (line mcantidad fecha if producto == 95) ///
		xtitle("Mes") ytitle("Demandada promedio (galones)") title("Demanda de Gasohol por producto" "y tipo de distrito") ///
