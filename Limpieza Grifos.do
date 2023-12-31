************************************TIE2*************************************
**************************David Ricardo y Yuri Solari*************************

clear all
cd /Users/yurisolari/Library/CloudStorage/OneDrive-UDEP/UDEP/2023/TIE/Data
use BD_grifos3.dta
egen id=group(COORDENADAS3)
gen year = substr(MESA_O,1,4) 
gen month = substr(MESA_O,6,.) 
rename COORDENADAS3 coordenadas
rename MESA_O my
rename PRECIO_DE_VENTA__SOLES_ precio
rename DISTRITO distrito
rename DEPARTAMENTO departamento
rename PROVINCIA provincia
rename PRODUCTO producto
drop departamento index 
order id provincia distrito coordenadas month year my precio buffer1 buffer2 buffer3
split coordenadas, p(", ")
gen latitud = substr(coordenadas1,2,.) 
gen longitud = substr(coordenadas2, 1, length(coordenadas2) - 1)
drop coordenadas1 coordenadas2
gen primera=substr(distrito,1,3)
replace distrito="BRENA" if primera=="BRE"
replace month="5" if month=="MAYO " 
drop primera

save bd, replace 

*primera base
keep id year month distrito buffer* latitud longitud producto coordenadas
save competencia, replace 
order id year month buffer1 buffer2 buffer3 distrito
sort id year month 

*comprobando consistencia 
by id buffer1, sort: gen nvals = _n == 1 
by id, sort: replace nvals = sum(nvals)
by id, sort: replace nvals = nvals[_N] 
drop nvals

sort id year month
drop year month
duplicates drop  
destring latitud longitud, replace
save competencia1, replace

geonear id latitud longitud using Pampilla, neighbors(id latitud longitud) ignoreself

*primera VI
egen meanclose = mean(km_to_nid), by(distrito producto)

*segunda VI
egen mbuffer1 = mean(buffer1), by(distrito)
egen mbuffer2 = mean(buffer2), by(distrito)
egen mbuffer3 = mean(buffer3), by(distrito)
save competenciagrifo, replace 

*base con VI
keep distrito meanclose mbuffer1 mbuffer2 mbuffer3 producto
duplicates drop
save competenciadist, replace

*base con precios
merge 1:m distrito producto using bd.dta

drop _merge
sort distrito year month producto id
order distrito year month producto id

*precio promedio del mes
egen mprecio = mean(precio), by(distrito year month producto)
keep distrito month year meanclose mbuffer1 mbuffer2 mbuffer3 provincia my mprecio producto

replace producto="84" if producto=="GASOHOL 84 PLUS"
replace producto="90" if producto=="GASOHOL 90 PLUS"
replace producto="95" if producto=="GASOHOL 95 PLUS"
replace producto="97" if producto=="GASOHOL 97 PLUS"
replace producto="98" if producto=="GASOHOL 98 PLUS"
destring producto, replace 
keep if producto==90 | producto==95
*replace distrito="BREÑA" if distrito=="BRE�A"
sort distrito year month
egen id=group(distrito year month)
duplicates drop 
save basefinal, replace 

*base de cantidades
clear
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
replace month="5" if month=="MAYO "
destring producto, replace
keep if producto==90 | producto==95 
drop primera

save cantidades, replace

*todo
clear
use basefinal
destring year producto, replace
merge 1:1 distrito year month producto using cantidades.dta 
drop if distrito=="ASIA" | distrito=="AUCALLAMA" | distrito=="BARRANCA" | distrito=="CANTA" | distrito=="CERRO AZUL" | distrito=="AUCALLAMA" | distrito=="CHANCAY" | distrito=="CHILCA" | distrito=="CUENCA" | distrito=="HUACHO" | distrito=="HUALMAY" | distrito=="HUARAL" | distrito=="HUAURA" | distrito=="IMPERIAL" | distrito=="LUNAHUANA" | distrito=="MALA" | distrito=="MATUCANA" | distrito=="NUEVO IMPERIAL" | distrito=="OYON" | distrito=="PARAMONGA" | distrito=="PATIVILCA" | distrito=="QUILMANA" | distrito=="RICARDO PALMA" | distrito=="SAN ANTONIO" | distrito=="SAN MATEO" | distrito=="SAN VICENTE DE CAÑETE" | distrito=="SANTA CRUZ DE COCACHACRA" | distrito=="SANTA EULALIA" | distrito=="SANTA MARIA" | distrito=="SANTA ROSA DE QUIVES" | distrito=="SANTO DOMINGO DE LOS OLLEROS" | distrito=="SAYAN" | distrito=="SUPE" | distrito=="VEGUETA" | distrito=="SUPE PUERTO"
drop if year==2020 & month=="1"
drop if year==2020 & month=="2"
destring month, replace
sort distrito year month producto
gen mis=0
replace mis=1 if cantidad==. | mprecio==.
tab mis
save basefinal, replace

*Número de distritos

clear
cd /Users/yurisolari/Library/CloudStorage/OneDrive-UDEP/UDEP/2023/TIE/Data
import excel NUM.xlsx, firstrow
gen primera=substr(distrito,1,3)
replace distrito="BRENA" if primera=="BRE"
drop primera
save num_dist, replace

*base con todo parte 2
clear
use basefinal
drop _merge
merge m:1 distrito using num_dist.dta
drop _merge
gen mcantidad=cantidad/num_dist
save, replace

drop mbuffer*


*Precios del petróleo crudo
clear
cd /Users/yurisolari/Library/CloudStorage/OneDrive-UDEP/UDEP/2023/TIE/Data
import excel Brent.xlsx, firstrow
gen year = substr(Date,7,4) 
gen month = substr(Date,1,2) 
destring year, replace
destring month, replace
drop Date g90 g95
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
save Brent.dta, replace

******************NUEVO
clear
cd /Users/yurisolari/Library/CloudStorage/OneDrive-UDEP/UDEP/2023/TIE/Data
use basefinal2.dta
keep distrito year month producto provincia my mprecio mcantidad buffer* 
order producto year month distrito mprecio mcantidad buffer*
sort producto year month distrito 

merge m:1 year month using Brent.dta
drop _merge
drop if distrito=="MI PERU"
drop in 1/12 
save, replace

**Determinar lag

ivregress 2sls mcantidad (mprecio=Brent)
estat firststage 
estat overid

*p value: 0
*R cuadrado:  0.7715
*Eigen-value: 10097.3

ivregress 2sls mcantidad (mprecio=lag1)
estat firststage 
estat overid

*p value: 0
*R cuadrado:  0.8520
*Eigen-value: 17215.1  

ivregress 2sls mcantidad (mprecio=lag2)
estat firststage 
estat overid

*p value: 0
*R cuadrado: 0.8736
*Eigen-value: 20668.3 

ivregress 2sls mcantidad (mprecio=lag3)
estat firststage 
estat overid

*p value: 0
*R cuadrado: 0.8393
*Eigen-value: 15626.4    

ivregress 2sls mcantidad (mprecio=lag4)
estat firststage 
estat overid

*p value: 0
*R cuadrado: 0.7755
*Eigen-value: 10330.1   

ivregress 2sls mcantidad (mprecio=lag5)
estat firststage 
estat overid


*BASEFINALLLLLL
keep producto year month distrito provincia mprecio mcantidad buffer41 lag2
drop if distrito=="Ml PERU"
drop if distrito=="PUNTA HERMOSA"
drop if distrito=="PUNTA NEGRA"
drop if distrito=="SANTA MARIA DEL MAR"
drop if distrito=="CARMEN DE LA LEGUA REYNOSO"
*BRENA: 11 grifos

*Corrigiendo Breña: 90
replace mcantidad=1485/11 if year==2020 & month==3 & distrito=="BRENA" &producto==90
replace mcantidad=117/11 if year==2020 & month==4 & distrito=="BRENA" &producto==90
replace mcantidad=760/11 if year==2020 & month==5 & distrito=="BRENA" &producto==90
replace mcantidad=760/11 if year==2020 & month==6 & distrito=="BRENA" &producto==90
replace mcantidad=2347/11 if year==2020 & month==7 & distrito=="BRENA" &producto==90
replace mcantidad=2087/11 if year==2020 & month==8 & distrito=="BRENA" &producto==90
replace mcantidad=2011/11 if year==2020 & month==9 & distrito=="BRENA" &producto==90
replace mcantidad=2211/11 if year==2020 & month==10 & distrito=="BRENA" &producto==90
replace mcantidad=1888/11 if year==2020 & month==11 & distrito=="BRENA" &producto==90
replace mcantidad=2329/11 if year==2020 & month==12 & distrito=="BRENA" &producto==90
replace mcantidad=2239/11 if year==2021 & month==1 & distrito=="BRENA" &producto==90
replace mcantidad=1969/11 if year==2021 & month==2 & distrito=="BRENA" &producto==90
replace mcantidad=2358/11 if year==2021 & month==3 & distrito=="BRENA" &producto==90
replace mcantidad=2483/11 if year==2021 & month==4 & distrito=="BRENA" &producto==90
replace mcantidad=2501/11 if year==2021 & month==5 & distrito=="BRENA" &producto==90
replace mcantidad=2602/11 if year==2021 & month==6 & distrito=="BRENA" &producto==90
replace mcantidad=2858/11 if year==2021 & month==7 & distrito=="BRENA" &producto==90
replace mcantidad=2858/11 if year==2021 & month==8 & distrito=="BRENA" &producto==90
replace mcantidad=2585/11 if year==2021 & month==9 & distrito=="BRENA" &producto==90
replace mcantidad=2585/11 if year==2021 & month==10 & distrito=="BRENA" &producto==90
replace mcantidad=2436/11 if year==2021 & month==11 & distrito=="BRENA" &producto==90
replace mcantidad=2794/11 if year==2021 & month==12 & distrito=="BRENA" &producto==90
replace mcantidad=1904/11 if year==2022 & month==1 & distrito=="BRENA" &producto==90
replace mcantidad=2555/11 if year==2022 & month==2 & distrito=="BRENA" &producto==90
replace mcantidad=2516/11 if year==2022 & month==3 & distrito=="BRENA" &producto==90
replace mcantidad=2201/11 if year==2022 & month==4 & distrito=="BRENA" &producto==90
replace mcantidad=2309/11 if year==2022 & month==5 & distrito=="BRENA" &producto==90
replace mcantidad=2117/11 if year==2022 & month==6 & distrito=="BRENA" &producto==90
replace mcantidad=1516/11 if year==2022 & month==7 & distrito=="BRENA" &producto==90
replace mcantidad=1919/11 if year==2022 & month==8 & distrito=="BRENA" &producto==90
replace mcantidad=1821/11 if year==2022 & month==9 & distrito=="BRENA" &producto==90
replace mcantidad=1769/11 if year==2022 & month==10 & distrito=="BRENA" &producto==90
replace mcantidad=1769/11 if year==2022 & month==11 & distrito=="BRENA" &producto==90
replace mcantidad=1677/11 if year==2022 & month==12 & distrito=="BRENA" &producto==90


replace mcantidad=1648/11 if year==2020 & month==3 & distrito=="BRENA" &producto==95
replace mcantidad=301/11 if year==2020 & month==4 & distrito=="BRENA" &producto==95
replace mcantidad=760/11 if year==2020 & month==5 & distrito=="BRENA" &producto==95
replace mcantidad=1457/11 if year==2020 & month==6 & distrito=="BRENA" &producto==95
replace mcantidad=2488/11 if year==2020 & month==7 & distrito=="BRENA" &producto==95
replace mcantidad=2348/11 if year==2020 & month==8 & distrito=="BRENA" &producto==95
replace mcantidad=2239/11 if year==2020 & month==9 & distrito=="BRENA" &producto==95
replace mcantidad=2533/11 if year==2020 & month==10 & distrito=="BRENA" &producto==95
replace mcantidad=2370/11 if year==2020 & month==11 & distrito=="BRENA" &producto==95
replace mcantidad=2824/11 if year==2020 & month==12 & distrito=="BRENA" &producto==95
replace mcantidad=2663/11 if year==2021 & month==1 & distrito=="BRENA" &producto==95
replace mcantidad=1841/11 if year==2021 & month==2 & distrito=="BRENA" &producto==95
replace mcantidad=2745/11 if year==2021 & month==3 & distrito=="BRENA" &producto==95
replace mcantidad=2618/11 if year==2021 & month==4 & distrito=="BRENA" &producto==95
replace mcantidad=2598/11 if year==2021 & month==5 & distrito=="BRENA" &producto==95
replace mcantidad=2744/11 if year==2021 & month==6 & distrito=="BRENA" &producto==95
replace mcantidad=2935/11 if year==2021 & month==7 & distrito=="BRENA" &producto==95
replace mcantidad=2664/11 if year==2021 & month==8 & distrito=="BRENA" &producto==95
replace mcantidad=3117/11 if year==2021 & month==9 & distrito=="BRENA" &producto==95
replace mcantidad=3258/11 if year==2021 & month==10 & distrito=="BRENA" &producto==95
replace mcantidad=3134/11 if year==2021 & month==11 & distrito=="BRENA" &producto==95
replace mcantidad=3355/11 if year==2021 & month==12 & distrito=="BRENA" &producto==95
replace mcantidad=468/11 if year==2022 & month==1 & distrito=="BRENA" &producto==95
replace mcantidad=607/11 if year==2022 & month==2 & distrito=="BRENA" &producto==95
replace mcantidad=3275/11 if year==2022 & month==3 & distrito=="BRENA" &producto==95
replace mcantidad=2602/11 if year==2022 & month==4 & distrito=="BRENA" &producto==95
replace mcantidad=2678/11 if year==2022 & month==5 & distrito=="BRENA" &producto==95
replace mcantidad=2283/11 if year==2022 & month==6 & distrito=="BRENA" &producto==95
replace mcantidad=1710/11 if year==2022 & month==7 & distrito=="BRENA" &producto==95
replace mcantidad=2242/11 if year==2022 & month==8 & distrito=="BRENA" &producto==95
replace mcantidad=1983/11 if year==2022 & month==9 & distrito=="BRENA" &producto==95
replace mcantidad=2118/11 if year==2022 & month==10 & distrito=="BRENA" &producto==95
replace mcantidad=2202/11 if year==2022 & month==11 & distrito=="BRENA" &producto==95
replace mcantidad=2355/11 if year==2022 & month==12 & distrito=="BRENA" &producto==95

save oficial, replace

*Obtener ingreso por distrito

clear all
cd "C:\Users\dipa_\OneDrive - UDEP\UDEP\2023\TIE\Data\Ingreso"
use enaho01a-2020-500.dta
keep ubigeo p524a1 p523 conglome vivienda hogar codperso
gen sal_anual=.
replace sal_anual=260*p524a1 if p523==1 
replace sal_anual=52*p524a1 if p523==2
replace sal_anual=24*p524a1 if p523==3
replace sal_anual=12*p524a1 if p523==4
gen year = 2020
egen id = concat(vivienda hogar)
collapse (sum) sal_anual, by(id ubigeo year)
collapse sal_anual, by(ubigeo year)
save 2020.dta, replace

clear
use enaho01a-2021-500.dta
keep ubigeo p524a1 p523 conglome vivienda hogar codperso
gen sal_anual=.
replace sal_anual=260*p524a1 if p523==1 
replace sal_anual=52*p524a1 if p523==2
replace sal_anual=24*p524a1 if p523==3
replace sal_anual=12*p524a1 if p523==4
gen year = 2021
egen id = concat(vivienda hogar)
collapse (sum) sal_anual, by(id ubigeo year)
collapse sal_anual, by(ubigeo year)
save 2021.dta, replace

clear
use enaho01a-2022-500.dta
keep ubigeo p524a1 p523 conglome vivienda hogar codperso
gen sal_anual=.
replace sal_anual=260*p524a1 if p523==1 
replace sal_anual=52*p524a1 if p523==2
replace sal_anual=24*p524a1 if p523==3
replace sal_anual=12*p524a1 if p523==4
gen year = 2021
egen id = concat(vivienda hogar)
collapse (sum) sal_anual, by(id ubigeo year)
collapse sal_anual, by(ubigeo year)
save 2022.dta, replace

clear
use 2020.dta 
append using 2021
append using 2022
save ingreso.dta, replace







