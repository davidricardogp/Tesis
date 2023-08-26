import pandas as pd
import googlemaps
import numpy as np
import swifter

import pandas as pd
import numpy as np
import os
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import geopandas 
import folium
from folium import plugins
import requests
import time
import geopandas as gpd

from shapely.geometry import Point, Polygon

lista_excels=[
"precios-2022_1_LMC",
"precios-2022_0_LMC",
"precios-2021_1_LMC",
"precios_2021_0_LMC",
"precios_2020_1_LMC",
"precios_2020_0_LMC"]

lista_hojas=["G84",
"G90",
"G95",
"G97",
"G98"]

pds=[]

for x in lista_excels:
    for i in lista_hojas:
        pds.append(pd.read_excel("{}.xlsx".format(x),sheet_name=i))

df=pd.concat(pds).reset_index()

df1=df.drop(["index"],axis=1)

df1["DIRECCIÓN"]=df1["DIRECCIÓN"].apply(lambda x: str(x).split("ESQUINA")[0].split("INTERSECCION")[0])

df1.loc[df1["DIRECCIÓN"]!="","DIRECCIÓN"]=df1["DIRECCIÓN"]+", "+df1["DISTRITO"]+", LIMA, PERU"

df3=df1.loc[df1["DIRECCIÓN"]!=""]

coord1=pd.DataFrame(df3["DIRECCIÓN"].value_counts()).reset_index()


gmaps = googlemaps.Client(key='AIzaSyBCWNE-WyVdUhB5Pp0DctKvyNnzdl3yQS0') # Esta llave ya no funciona

def geo(x):
    try:
        geoc=gmaps.geocode(x)[0]["geometry"]["location"]
        return (geoc["lat"],geoc["lng"])
    except:
        return np.nan

coord1["COORDENADAS"]=coord1["index"].swifter.apply(lambda x: geo(x))

coord2=coord1.drop(["DIRECCIÓN"],axis=1).rename(columns={"index":"DIRECCIÓN"})

df4=df1.merge(coord2, how="left",on="DIRECCIÓN")

df5=df4.loc[df4["DIRECCIÓN"]!=""].reset_index()
lista_coord=list(df4.loc[df4["COORDENADAS"].isna()==False]["COORDENADAS"].value_counts().index)


a=geopandas.read_file("distritos-peru/distritos-peru.shp",encoding="utf-8")

a1=a.loc[a["nombdep"]=="LIMA"]
a2_1=a1.loc[a1["nombprov"]=="LIMA"]
a2_2=a.loc[a["nombprov"]=="CALLAO"]
a3=pd.concat([a2_1,a2_2])

mapa1=folium.Map(location = [-12.085,-77.04], tiles='OpenStreetMap', zoom_start = 6)

df6=df5.loc[df5["COORDENADAS"].isna()==False]
df7=pd.DataFrame(df6.groupby(["COORDENADAS","DIRECCIÓN","DISTRITO","RAZÓN SOCIAL","RUC"])["UNIDAD"].count()).reset_index()

folium.GeoJson(data=a3["geometry"],style_function=lambda x: {"color":"black","weight":1,"fillOpacity":0}).add_to(mapa1)

df8=df7.merge(a3.rename(columns={"nombdist":"DISTRITO"})[["DISTRITO","geometry"]])

df8_coord=list(df8["COORDENADAS"].apply(lambda x: Point(x[1],x[0])))
df8_geometry=list(df8["geometry"])
df8_within=[]

for x in range(len(df8_coord)):
    df8_within.append(df8_coord[x].within(df8_geometry[x]))
    
df8["within"]=df8_within

def color(x):
    if x==False:
        return "Red"
    else:
        return "Blue"

df8["color"]=df8["within"].apply(lambda x: color(x))

for x in range(len(list(df8["COORDENADAS"]))):
    mapa1.add_child(folium.CircleMarker(location = df8["COORDENADAS"][x], popup = df8["DIRECCIÓN"][x],radius=2,color=df8["color"][x]))
    
mapa1

rev1=pd.read_excel("coordenadas/coordenadas1.xlsx")
rev2=pd.read_excel("coordenadas/coordenadas2.xlsx")
rev3=pd.DataFrame(rev1.groupby(["DIRECCIÓN","CORDENADAS"])["UNIDAD"].count()).reset_index()[["DIRECCIÓN","CORDENADAS"]].rename(columns={"CORDENADAS":"COORDENADAS"})
rev4=pd.DataFrame(rev2.groupby(["DIRECCIÓN","CORRECIÓN"])["RUC"].count()).reset_index()[["DIRECCIÓN","CORRECIÓN"]].rename(columns={"CORRECIÓN":"COORDENADAS"})
rev5=pd.concat([rev3,rev4]).reset_index()[["DIRECCIÓN","COORDENADAS"]]
rev5["COORDENADAS2"]=rev5["COORDENADAS"].apply(lambda x: (-abs(float(x.split(", ")[0])),float(x.split(", ")[1])))

bd1=df4.merge(rev5[["DIRECCIÓN","COORDENADAS2"]],on="DIRECCIÓN",how="left")
bd1.loc[bd1["COORDENADAS2"].apply(lambda x: str(x))=="nan","COORDENADAS2"]=bd1["COORDENADAS"]

reb1=pd.read_excel("Coordenadas corregidas 2.xlsx")
reb1["CORRECCIÓN"]=reb1["CORRECCIÓN"].apply(lambda x: x[1:-1])
reb1["COORDENADAS3"]=reb1["CORRECCIÓN"].apply(lambda x: (float(x.split(", ")[0]),float(x.split(", ")[1])))
reb2=pd.DataFrame(reb1.groupby(["DIRECCIÓN","COORDENADAS3"])["RUC"].count()).reset_index()[["DIRECCIÓN","COORDENADAS3"]]

bd2=bd1.merge(reb2,on="DIRECCIÓN",how="left")
bd2.loc[bd2["COORDENADAS3"].apply(lambda x: str(x))=="nan","COORDENADAS3"]=bd2["COORDENADAS2"]
bd2.loc[bd2["COORDENADAS3"]==(-12.107354, -77.010644),"COORDENADAS3"] = "hola"

def COORD(x):
    if x=="hola":
        return (-11.833344, -77.157746)
    else:
        return x

bd2["COORDENADAS3"]=bd2["COORDENADAS3"].apply(lambda x: COORD(x))

mapa1=folium.Map(location = [-12.085,-77.04], tiles='OpenStreetMap', zoom_start = 6)
folium.LatLngPopup().add_to(mapa1)

df7=pd.DataFrame(bd2.groupby(["COORDENADAS3","DIRECCIÓN","DISTRITO","RAZÓN SOCIAL","RUC"])["UNIDAD"].count()).reset_index()

folium.GeoJson(data=a3["geometry"],style_function=lambda x: {"color":"black","weight":1,"fillOpacity":0}).add_to(mapa1)

df8=df7.merge(a3.rename(columns={"nombdist":"DISTRITO"})[["DISTRITO","geometry"]])

df8_coord=list(df8["COORDENADAS3"].apply(lambda x: Point(x[1],x[0])))
df8_geometry=list(df8["geometry"])
df8_within=[]

for x in range(len(df8_coord)):
    df8_within.append(df8_coord[x].within(df8_geometry[x]))
    
df8["within"]=df8_within

def color(x):
    if x==False:
        return "Red"
    else:
        return "Blue"

df8["color"]=df8["within"].apply(lambda x: color(x))

for x in range(len(list(df8["COORDENADAS3"]))):
    mapa1.add_child(folium.CircleMarker(location = df8["COORDENADAS3"][x], popup = "{} /// {}".format(df8["DIRECCIÓN"][x],df8["COORDENADAS3"][x]),radius=2,color=df8["color"][x]))
    
mapa1

df7=pd.DataFrame(bd2.groupby(["COORDENADAS3","DIRECCIÓN","DISTRITO","RAZÓN SOCIAL","RUC"])["UNIDAD"].count()).reset_index()

folium.GeoJson(data=a3["geometry"],style_function=lambda x: {"color":"black","weight":1,"fillOpacity":0}).add_to(mapa1)

df8=df7.merge(a3.rename(columns={"nombdist":"DISTRITO"})[["DISTRITO","geometry"]])

df8["points"]=df8["COORDENADAS3"].apply(lambda x: Point(x[1],x[0]))

gdf = geopandas.GeoDataFrame(df8, geometry=df8["points"])

gdf["geometry1"] = gdf["geometry"]
gdf['geometry1'] = gdf.geometry1.buffer(0.002)

gdf["geometry2"] = gdf["geometry"]
gdf['geometry2'] = gdf.geometry2.buffer(0.004)

gdf["geometry3"] = gdf["geometry"]
gdf['geometry3'] = gdf.geometry3.buffer(0.007)

mapa1=folium.Map(location = [-12.085,-77.04], tiles='OpenStreetMap', zoom_start = 6)
folium.LatLngPopup().add_to(mapa1)

folium.GeoJson(data=gdf["geometry1"],style_function=lambda x: {"color":"black","weight":1,"fillOpacity":0}).add_to(mapa1)
    
mapa1

list_points=set(list(gdf["points"]))

def withinx(i):
    lista123=[]
    for n in list_points:
        if n.within(i) == True:
            lista123.append(n)
    return len(lista123)
    

gdf["buffer1"]=gdf["geometry1"].swifter.apply(lambda x: withinx(x))
gdf["buffer2"]=gdf["geometry2"].swifter.apply(lambda x: withinx(x))
gdf["buffer3"]=gdf["geometry3"].swifter.apply(lambda x: withinx(x))

buffers=pd.DataFrame(gdf.groupby(["COORDENADAS3","buffer1","buffer2","buffer3"])["UNIDAD"].count()).reset_index().iloc[:,:4]

bd3=bd2.drop(columns=["COORDENADAS","COORDENADAS2"]).merge(buffers,on="COORDENADAS3",how="left")
bd3["REGISTRO DE HIDROCARBUROS"]=bd3["REGISTRO DE HIDROCARBUROS"].apply(lambda x: str(x))
bd3["COORDENADAS3"]=bd3["COORDENADAS3"].apply(lambda x: str(x))
# bd3.to_stata("BD_grifos.dta")

import pandas as pd

gf=pd.read_stata("BD_grifos.dta")

grifeiros=pd.read_excel("BD_grifeiros.xlsx")

for x in range(grifeiros.shape[0]):
    gf.loc[(gf["RAZ_N_SOCIAL"]==grifeiros["RAZ_N_SOCIAL"][x]) & (gf["DISTRITO"]==grifeiros["DISTRITO"][x]),"DIRECCI_N"]=grifeiros["DIRECCI_N"][x]
    gf.loc[(gf["RAZ_N_SOCIAL"]==grifeiros["RAZ_N_SOCIAL"][x]) & (gf["DISTRITO"]==grifeiros["DISTRITO"][x]),"COORDENADAS3"]=grifeiros["COORDENADAS3"].apply(lambda x: "("+x+")")[x]
    
gf["COORDENADAS3"]=gf["COORDENADAS3"].apply(lambda x: (float(x[1:-1].split(", ")[0]),float(x[1:-1].split(", ")[1])))

gf2=gf.drop(columns=["buffer1","buffer2","buffer3"])

df7=pd.DataFrame(gf2.groupby(["COORDENADAS3","DIRECCI_N","DISTRITO","RAZ_N_SOCIAL","RUC"])["UNIDAD"].count()).reset_index()

a=geopandas.read_file("distritos-peru/distritos-peru.shp",encoding="utf-8")

a1=a.loc[a["nombdep"]=="LIMA"]
a2_1=a1.loc[a1["nombprov"]=="LIMA"]
a2_2=a.loc[a["nombprov"]=="CALLAO"]
a3=pd.concat([a2_1,a2_2])

folium.GeoJson(data=a3["geometry"],style_function=lambda x: {"color":"black","weight":1,"fillOpacity":0}).add_to(mapa1)

df8=df7.merge(a3.rename(columns={"nombdist":"DISTRITO"})[["DISTRITO","geometry"]])

df8["points"]=df8["COORDENADAS3"].apply(lambda x: Point(x[1],x[0]))

gdf = geopandas.GeoDataFrame(df8, geometry=df8["points"])
gdf["geometry1"] = gdf["geometry"]
gdf['geometry1'] = gdf.geometry1.buffer(0.0045)

gdf["geometry2"] = gdf["geometry"]
gdf['geometry2'] = gdf.geometry2.buffer(0.004)

gdf["geometry3"] = gdf["geometry"]
gdf['geometry3'] = gdf.geometry3.buffer(0.007)

mapa1=folium.Map(location = [-12.085,-77.04], tiles='OpenStreetMap', zoom_start = 6)
folium.LatLngPopup().add_to(mapa1)

folium.GeoJson(data=gdf["geometry1"],style_function=lambda x: {"color":"black","weight":1,"fillOpacity":0}).add_to(mapa1)

mapa1

a=geopandas.read_file("distritos-peru/distritos-peru.shp",encoding="utf-8")

a1=a.loc[a["nombdep"]=="LIMA"]
a2_1=a1.loc[a1["nombprov"]=="LIMA"]
a2_2=a.loc[a["nombprov"]=="CALLAO"]
a3=pd.concat([a2_1,a2_2])

mapa1=folium.Map(location = [-12.085,-77.04], tiles='OpenStreetMap', zoom_start = 6)


folium.LatLngPopup().add_to(mapa1)

df7=pd.DataFrame(gf2.groupby(["COORDENADAS3","DIRECCI_N","DISTRITO","RAZ_N_SOCIAL","RUC"])["UNIDAD"].count()).reset_index()

folium.GeoJson(data=a3["geometry"],style_function=lambda x: {"color":"black","weight":1,"fillOpacity":0}).add_to(mapa1)

df8=df7.merge(a3.rename(columns={"nombdist":"DISTRITO"})[["DISTRITO","geometry"]])

df8_coord=list(df8["COORDENADAS3"].apply(lambda x: Point(x[1],x[0])))
df8_geometry=list(df8["geometry"])
df8_within=[]

for x in range(len(df8_coord)):
    df8_within.append(df8_coord[x].within(df8_geometry[x]))
    
df8["within"]=df8_within

def color(x):
    if x==False:
        return "Blue"
    else:
        return "Blue"

df8["color"]=df8["within"].apply(lambda x: color(x))

folium.GeoJson(data=gdf["geometry3"],style_function=lambda x: {"color":"black","weight":1,"fillOpacity":0}).add_to(mapa1)

for x in range(len(list(df8["COORDENADAS3"]))):
    mapa1.add_child(folium.CircleMarker(location = df8["COORDENADAS3"][x], popup = "{} /// {}".format(df8["DIRECCI_N"][x],df8["COORDENADAS3"][x]),radius=2,color=df8["color"][x]))
    
mapa1

list_points=set(list(gdf["points"]))

def withinx(i):
    lista123=[]
    for n in list_points:
        if n.within(i) == True:
            lista123.append(n)
    return len(lista123)
    

gdf["buffer1"]=gdf["geometry1"].swifter.apply(lambda x: withinx(x))
gdf["buffer2"]=gdf["geometry2"].swifter.apply(lambda x: withinx(x))
gdf["buffer3"]=gdf["geometry3"].swifter.apply(lambda x: withinx(x))

buffers=pd.DataFrame(gdf.groupby(["COORDENADAS3","buffer1","buffer2","buffer3"])["UNIDAD"].count()).reset_index().iloc[:,:4]

gf3=gf2.merge(buffers,on="COORDENADAS3",how="left")

gf3["REGISTRO_DE_HIDROCARBUROS"]=gf3["REGISTRO_DE_HIDROCARBUROS"].apply(lambda x: str(x))
gf3["COORDENADAS3"]=gf3["COORDENADAS3"].apply(lambda x: str(x))

gf3.reset_index().iloc[:,2:].to_stata("BD_grifos2.dta",version=118)

import pandas as pd

grifeiros2=pd.read_stata("BD_grifos2.dta")

grifeiros2["MESAÑO"]=grifeiros2["FECHA_DE_REGISTRO"].apply(lambda x: str(x.year)+"-"+str(x.month))

grifeiros2.groupby(["COORDENADAS3","MESAÑO","PRODUCTO"])[["PRECIO_DE_VENTA__SOLES_","buffer1","buffer2","buffer3"]].mean().reset_index()

grifeiros3=grifeiros2.groupby(["COORDENADAS3","MESAÑO","PRODUCTO"])[["PRECIO_DE_VENTA__SOLES_","buffer1","buffer2","buffer3"]].mean().reset_index().merge(grifeiros2.groupby(["COORDENADAS3","DISTRITO","DEPARTAMENTO","PROVINCIA"])[["REGISTRO_DE_HIDROCARBUROS"]].count().reset_index().drop(columns=["REGISTRO_DE_HIDROCARBUROS"]),on="COORDENADAS3",how="left")
grifeiros3.to_stata("BD_grifos3.dta")

import pandas as pd

gf=pd.read_stata("BD_grifos.dta")

grifeiros=pd.read_excel("BD_grifeiros.xlsx")

for x in range(grifeiros.shape[0]):
    gf.loc[(gf["RAZ_N_SOCIAL"]==grifeiros["RAZ_N_SOCIAL"][x]) & (gf["DISTRITO"]==grifeiros["DISTRITO"][x]),"DIRECCI_N"]=grifeiros["DIRECCI_N"][x]
    gf.loc[(gf["RAZ_N_SOCIAL"]==grifeiros["RAZ_N_SOCIAL"][x]) & (gf["DISTRITO"]==grifeiros["DISTRITO"][x]),"COORDENADAS3"]=grifeiros["COORDENADAS3"].apply(lambda x: "("+x+")")[x]
    
gf["COORDENADAS3"]=gf["COORDENADAS3"].apply(lambda x: (float(x[1:-1].split(", ")[0]),float(x[1:-1].split(", ")[1])))

gf2=gf.drop(columns=["buffer1","buffer2","buffer3"])


df7=pd.DataFrame(gf2.groupby(["COORDENADAS3","DIRECCI_N","DISTRITO","RAZ_N_SOCIAL","RUC"])["UNIDAD"].count()).reset_index()


a=geopandas.read_file("distritos-peru/distritos-peru.shp",encoding="utf-8")

a1=a.loc[a["nombdep"]=="LIMA"]
a2_1=a1.loc[a1["nombprov"]=="LIMA"]
a2_2=a.loc[a["nombprov"]=="CALLAO"]
a3=pd.concat([a2_1,a2_2])


folium.GeoJson(data=a3["geometry"],style_function=lambda x: {"color":"black","weight":1,"fillOpacity":0}).add_to(mapa1)

df8=df7.merge(a3.rename(columns={"nombdist":"DISTRITO"})[["DISTRITO","geometry"]])

df8["points"]=df8["COORDENADAS3"].apply(lambda x: Point(x[1],x[0]))

gdf = geopandas.GeoDataFrame(df8, geometry=df8["points"])

list_points=set(list(gdf["points"]))

def withinx(i):
    lista123=[]
    for n in list_points:
        if n.within(i) == True:
            lista123.append(n)
    return len(lista123)

all_buffers={}

for x in range(100):
    print(x)
    all_buffers["buffer{}".format(x+1)]=gdf["geometry"].buffer(0.0001*(x+1)).swifter.apply(lambda x: withinx(x))

buffers0=pd.concat([gdf,pd.DataFrame(all_buffers)],axis=1)

buffers=buffers0[["COORDENADAS3"]+["buffer{}".format(x+1) for x in range(100)]].drop_duplicates().reset_index(drop=True)

gf3=gf2.merge(buffers,on="COORDENADAS3",how="left").drop(columns=["index"])

gf3["REGISTRO_DE_HIDROCARBUROS"]=gf3["REGISTRO_DE_HIDROCARBUROS"].apply(lambda x: str(x))
gf3["COORDENADAS3"]=gf3["COORDENADAS3"].apply(lambda x: str(x))

grifeiros2=gf3

grifeiros2["my"]=grifeiros2["FECHA_DE_REGISTRO"].apply(lambda x: "{}-{}".format(x.year,x.month))
grifeiros2["distrito"]=grifeiros2["DISTRITO"]
grifeiros2["producto"]=grifeiros2["PRODUCTO"].apply(lambda x: float(x[8:10]))

grifeiros3=grifeiros2.groupby(["distrito","my","producto"])[["buffer{}".format(x+1) for x in range(100)]].mean().reset_index()

grifeiros3["key"] = grifeiros3["distrito"].apply(lambda x: str(x).replace("Ñ","N")) + "-" + grifeiros3["my"].apply(lambda x: str(x))+ "-" + grifeiros3["producto"].apply(lambda x: str(x))

grifeiros3=grifeiros3.drop(columns=["distrito","my","producto"])

bf=pd.read_stata("basefinal.dta")

bf["distrito"]=bf["distrito"].apply(lambda x: x.replace("Ñ","N"))

bf["key"] = bf["distrito"].apply(lambda x: str(x)) + "-" + bf["my"].apply(lambda x: str(x))+ "-" + bf["producto"].apply(lambda x: str(x))

bf2=bf.merge(grifeiros3,how="left",on="key")

bf2["distrito"]=bf2["distrito"].apply(lambda x: x.replace("Ñ","N"))

bf2.to_stata("basefinal2.dta")