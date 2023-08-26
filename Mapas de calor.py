import pandas as pd
import numpy as np
import os
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import geopandas
import folium
from folium import plugins
import requests
from shapely.geometry import Polygon
import time

import pandas as pd
import numpy as np
import geopandas
import folium
import matplotlib.pyplot as plt
from folium import plugins


# finalplis=pd.read_stata("finalplis.dta")
a=geopandas.read_file('distritos-peru/distritos-peru.shp',encoding="utf-8")
finalplis0=pd.read_stata("final.dta")

finalplis1=finalplis0[["distrito","mbuffer"]].groupby(["distrito"]).mean().reset_index()
finalplis1.loc[(finalplis1["distrito"].apply(lambda x: x in list(a["nombdist"]))==False)&(finalplis1["distrito"].apply(lambda x: "BRE" in str(x))),"distrito"]="BREÑA"
finalplis1.loc[(finalplis1["distrito"].apply(lambda x: x in list(a["nombdist"]))==False)&(finalplis1["distrito"].apply(lambda x: "MAG" in str(x))),"distrito"]="MAGDALENA DEL MAR"

finalplis=finalplis1.rename(columns={"distrito":"nombdist","mbuffer":"total"})

a1=a.loc[(a["nombprov"]=="LIMA")|(a["nombdep"].apply(lambda x: "CALLAO" in x))]

a1_0=a1.merge(finalplis, how="left", on="nombdist")

a3=a1_0.loc[a1_0["total"].isna()==False].copy()

colores=list(reversed([
'#1c2475','#18297a','#122e7f','#083385','#00388a','#003d8f',
'#004293','#004798','#004b9d','#0050a1','#0055a6','#005aaa',
'#005fae','#0063b2','#0068b6','#006dba','#0072bd','#0077c1',
'#007cc4','#0080c8','#0085cb','#008ace','#008fd1','#0094d4',
'#0099d7','#009dda','#00a2dc','#00a7df','#00ace1','#00b1e4',
'#00b6e6','#00bae8','#00bfeb','#00c4ed','#00c9ef','#00cef1',
'#00d3f3','#00d7f4','#00dcf6','#1ae1f8']))

bins=np.linspace(min(a3["total"].apply(lambda x: float(x))),max(a3['total'].apply(lambda x: float(x))),len(colores)+1)
a3['color']=pd.cut(a3["total"],bins,labels=colores,include_lowest=True)


a4=a1_0.loc[a1_0["total"].isna()==True].copy()
a4["color"]="#DADADA"


mapa0 = folium.Map(location=[-12.05, -76.9], zoom_start=10, tiles="Cartodb Positron")
folium.LatLngPopup().add_to(mapa0)

def heatmap(x):
    for _, ñ in a3.iloc[x:x+1,:].iterrows():
        sim_geo = geopandas.GeoSeries(ñ['geometry']).simplify(tolerance=0.001)
        geo_j = sim_geo.to_json()
        geo_j = folium.GeoJson(data=geo_j,
                               style_function=lambda x: {'fillColor': ñ["color"],"color":"black","weight": 1.3,"fillOpacity":1})
        folium.Popup(str(ñ["nombdist"])+": "+str(ñ["total"])).add_to(geo_j)
        geo_j.add_to(mapa0)
        
def heatmap2(x):
    for _, ñ in a4.iloc[x:x+1,:].iterrows():
        sim_geo = geopandas.GeoSeries(ñ['geometry']).simplify(tolerance=0.001)
        geo_j = sim_geo.to_json()
        geo_j = folium.GeoJson(data=geo_j,
                               style_function=lambda x: {'fillColor': ñ["color"],"color":"black","weight": 1.3,"fillOpacity":1})
        folium.Popup(str(ñ["nombdist"])+": "+str(ñ["total"])).add_to(geo_j)
        geo_j.add_to(mapa0)

for x in range(a3.shape[0]):
    heatmap(x)
    
for x in range(a4.shape[0]):
    heatmap2(x)  

mapa0

finalplis1=finalplis0[["distrito","pobreza"]].groupby(["distrito"]).mean().reset_index()
finalplis1.loc[(finalplis1["distrito"].apply(lambda x: x in list(a["nombdist"]))==False)&(finalplis1["distrito"].apply(lambda x: "BRE" in str(x))),"distrito"]="BREÑA"
finalplis1.loc[(finalplis1["distrito"].apply(lambda x: x in list(a["nombdist"]))==False)&(finalplis1["distrito"].apply(lambda x: "MAG" in str(x))),"distrito"]="MAGDALENA DEL MAR"

finalplis=finalplis1.rename(columns={"distrito":"nombdist","pobreza":"total"})

a1=a.loc[(a["nombprov"]=="LIMA")|(a["nombdep"].apply(lambda x: "CALLAO" in x))]

a1_0=a1.merge(finalplis, how="left", on="nombdist")

a3=a1_0.loc[a1_0["total"].isna()==False].copy()

colores=list(reversed([
'#1c2475','#18297a','#122e7f','#083385','#00388a','#003d8f',
'#004293','#004798','#004b9d','#0050a1','#0055a6','#005aaa',
'#005fae','#0063b2','#0068b6','#006dba','#0072bd','#0077c1',
'#007cc4','#0080c8','#0085cb','#008ace','#008fd1','#0094d4',
'#0099d7','#009dda','#00a2dc','#00a7df','#00ace1','#00b1e4',
'#00b6e6','#00bae8','#00bfeb','#00c4ed','#00c9ef','#00cef1',
'#00d3f3','#00d7f4','#00dcf6','#1ae1f8']))

bins=np.linspace(min(a3["total"].apply(lambda x: float(x))),max(a3['total'].apply(lambda x: float(x))),len(colores)+1)
a3['color']=pd.cut(a3["total"],bins,labels=colores,include_lowest=True)


a4=a1_0.loc[a1_0["total"].isna()==True].copy()
a4["color"]="#DADADA"


mapa0 = folium.Map(location=[-12.05, -76.9], zoom_start=10, tiles="Cartodb Positron")
folium.LatLngPopup().add_to(mapa0)

def heatmap(x):
    for _, ñ in a3.iloc[x:x+1,:].iterrows():
        sim_geo = geopandas.GeoSeries(ñ['geometry']).simplify(tolerance=0.001)
        geo_j = sim_geo.to_json()
        geo_j = folium.GeoJson(data=geo_j,
                               style_function=lambda x: {'fillColor': ñ["color"],"color":"black","weight": 1.3,"fillOpacity":1})
        folium.Popup(str(ñ["nombdist"])+": "+str(ñ["total"])).add_to(geo_j)
        geo_j.add_to(mapa0)
        
def heatmap2(x):
    for _, ñ in a4.iloc[x:x+1,:].iterrows():
        sim_geo = geopandas.GeoSeries(ñ['geometry']).simplify(tolerance=0.001)
        geo_j = sim_geo.to_json()
        geo_j = folium.GeoJson(data=geo_j,
                               style_function=lambda x: {'fillColor': ñ["color"],"color":"black","weight": 1.3,"fillOpacity":1})
        folium.Popup(str(ñ["nombdist"])+": "+str(ñ["total"])).add_to(geo_j)
        geo_j.add_to(mapa0)

for x in range(a3.shape[0]):
    heatmap(x)
    
for x in range(a4.shape[0]):
    heatmap2(x)  

mapa0

finalplis0=pd.read_stata("GASOLINA 90.dta")

finalplis1=finalplis0.loc[finalplis0["producto"].apply(lambda x: "0" in str(x))].groupby(["distrito"])[["cantidad"]].mean().reset_index()
finalplis1.loc[(finalplis1["distrito"].apply(lambda x: x in list(a["nombdist"]))==False)&(finalplis1["distrito"].apply(lambda x: "BRE" in str(x))),"distrito"]="BREÑA"
finalplis1.loc[(finalplis1["distrito"].apply(lambda x: x in list(a["nombdist"]))==False)&(finalplis1["distrito"].apply(lambda x: "MAG" in str(x))),"distrito"]="MAGDALENA DEL MAR"

finalplis=finalplis1.rename(columns={"distrito":"nombdist","cantidad":"total"})

a1=a.loc[(a["nombprov"]=="LIMA")|(a["nombdep"].apply(lambda x: "CALLAO" in x))]

a1_0=a1.merge(finalplis, how="left", on="nombdist")

a3=a1_0.loc[a1_0["total"].isna()==False].copy()

colores=list(reversed([
'#1c2475','#18297a','#122e7f','#083385','#00388a','#003d8f',
'#004293','#004798','#004b9d','#0050a1','#0055a6','#005aaa',
'#005fae','#0063b2','#0068b6','#006dba','#0072bd','#0077c1',
'#007cc4','#0080c8','#0085cb','#008ace','#008fd1','#0094d4',
'#0099d7','#009dda','#00a2dc','#00a7df','#00ace1','#00b1e4',
'#00b6e6','#00bae8','#00bfeb','#00c4ed','#00c9ef','#00cef1',
'#00d3f3','#00d7f4','#00dcf6','#1ae1f8']))

bins=np.linspace(min(a3["total"].apply(lambda x: float(x))),max(a3['total'].apply(lambda x: float(x))),len(colores)+1)
a3['color']=pd.cut(a3["total"],bins,labels=colores,include_lowest=True)


a4=a1_0.loc[a1_0["total"].isna()==True].copy()
a4["color"]="#DADADA"


mapa0 = folium.Map(location=[-12.05, -76.9], zoom_start=10, tiles="Cartodb Positron")
folium.LatLngPopup().add_to(mapa0)

def heatmap(x):
    for _, ñ in a3.iloc[x:x+1,:].iterrows():
        sim_geo = geopandas.GeoSeries(ñ['geometry']).simplify(tolerance=0.001)
        geo_j = sim_geo.to_json()
        geo_j = folium.GeoJson(data=geo_j,
                               style_function=lambda x: {'fillColor': ñ["color"],"color":"black","weight": 1.3,"fillOpacity":1})
        folium.Popup(str(ñ["nombdist"])+": "+str(ñ["total"])).add_to(geo_j)
        geo_j.add_to(mapa0)
        
def heatmap2(x):
    for _, ñ in a4.iloc[x:x+1,:].iterrows():
        sim_geo = geopandas.GeoSeries(ñ['geometry']).simplify(tolerance=0.001)
        geo_j = sim_geo.to_json()
        geo_j = folium.GeoJson(data=geo_j,
                               style_function=lambda x: {'fillColor': ñ["color"],"color":"black","weight": 1.3,"fillOpacity":1})
        folium.Popup(str(ñ["nombdist"])+": "+str(ñ["total"])).add_to(geo_j)
        geo_j.add_to(mapa0)

for x in range(a3.shape[0]):
    heatmap(x)
    
for x in range(a4.shape[0]):
    heatmap2(x)  

mapa0

finalplis0=pd.read_stata("GASOLINA 95.dta")

finalplis1=finalplis0.loc[finalplis0["producto"].apply(lambda x: "5" in str(x))].groupby(["distrito"])[["cantidad"]].mean().reset_index()
finalplis1.loc[(finalplis1["distrito"].apply(lambda x: x in list(a["nombdist"]))==False)&(finalplis1["distrito"].apply(lambda x: "BRE" in str(x))),"distrito"]="BREÑA"
finalplis1.loc[(finalplis1["distrito"].apply(lambda x: x in list(a["nombdist"]))==False)&(finalplis1["distrito"].apply(lambda x: "MAG" in str(x))),"distrito"]="MAGDALENA DEL MAR"

finalplis=finalplis1.rename(columns={"distrito":"nombdist","cantidad":"total"})

a1=a.loc[(a["nombprov"]=="LIMA")|(a["nombdep"].apply(lambda x: "CALLAO" in x))]

a1_0=a1.merge(finalplis, how="left", on="nombdist")

a3=a1_0.loc[a1_0["total"].isna()==False].copy()

colores=list(reversed([
'#1c2475','#18297a','#122e7f','#083385','#00388a','#003d8f',
'#004293','#004798','#004b9d','#0050a1','#0055a6','#005aaa',
'#005fae','#0063b2','#0068b6','#006dba','#0072bd','#0077c1',
'#007cc4','#0080c8','#0085cb','#008ace','#008fd1','#0094d4',
'#0099d7','#009dda','#00a2dc','#00a7df','#00ace1','#00b1e4',
'#00b6e6','#00bae8','#00bfeb','#00c4ed','#00c9ef','#00cef1',
'#00d3f3','#00d7f4','#00dcf6','#1ae1f8']))

bins=np.linspace(min(a3["total"].apply(lambda x: float(x))),max(a3['total'].apply(lambda x: float(x))),len(colores)+1)
a3['color']=pd.cut(a3["total"],bins,labels=colores,include_lowest=True)


a4=a1_0.loc[a1_0["total"].isna()==True].copy()
a4["color"]="#DADADA"


mapa0 = folium.Map(location=[-12.05, -76.9], zoom_start=10, tiles="Cartodb Positron")
folium.LatLngPopup().add_to(mapa0)

def heatmap(x):
    for _, ñ in a3.iloc[x:x+1,:].iterrows():
        sim_geo = geopandas.GeoSeries(ñ['geometry']).simplify(tolerance=0.001)
        geo_j = sim_geo.to_json()
        geo_j = folium.GeoJson(data=geo_j,
                               style_function=lambda x: {'fillColor': ñ["color"],"color":"black","weight": 1.3,"fillOpacity":1})
        folium.Popup(str(ñ["nombdist"])+": "+str(ñ["total"])).add_to(geo_j)
        geo_j.add_to(mapa0)
        
def heatmap2(x):
    for _, ñ in a4.iloc[x:x+1,:].iterrows():
        sim_geo = geopandas.GeoSeries(ñ['geometry']).simplify(tolerance=0.001)
        geo_j = sim_geo.to_json()
        geo_j = folium.GeoJson(data=geo_j,
                               style_function=lambda x: {'fillColor': ñ["color"],"color":"black","weight": 1.3,"fillOpacity":1})
        folium.Popup(str(ñ["nombdist"])+": "+str(ñ["total"])).add_to(geo_j)
        geo_j.add_to(mapa0)

for x in range(a3.shape[0]):
    heatmap(x)
    
for x in range(a4.shape[0]):
    heatmap2(x)  

mapa0
