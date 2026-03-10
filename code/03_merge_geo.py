"""
03_merge_geodata.py
────────────────────────────────────────────────────────────────────────────────
Merges ECF_total.csv con Plotly GeoJSON de los condados de US y produce un GeoDataFrame listo para graficar. 
Se asegura de que el campo FIPS esté en formato string de 5 dígitos en ambos datasets antes de hacer el merge. 
El resultado es un GeoDataFrame con geometrías de condados y atributos ECF, que se guarda como GeoJSON para su uso en la visualización.

Inputs
------
  data/raw/ECF_total.csv              
  data/raw/geojson-counties-fips.json US county geometries (Plotly public dataset)

Outputs
-------
  data/processed/merged_ecf_counties.geojson  GeoJSON con geometrías de condados y 
  atributos ECF para graficar

Uso
-----
  python 03_merge_geodata.py

Requirimientos
------------
  pip install pandas geopandas 
"""
import pandas as pd
import geopandas as gpd

geojson_path = "data/raw/geojson-counties-fips.json"     
ecf_path = "data/raw/ECF_total.csv"

# --- CARGAR ---
gdf = gpd.read_file(geojson_path)
ecf = pd.read_csv(ecf_path)


# --- CREAR FIPS EN GEOJSON (string 5 dígitos) ---
gdf["FIPS"] = gdf["STATE"].astype(str).str.zfill(2) + gdf["COUNTY"].astype(str).str.zfill(3)    

# --- ASEGURAR FIPS EN ECF (string 5 dígitos) ---
ecf["FIPS"] = pd.to_numeric(ecf["FIPS"], errors="coerce").astype("Int64").astype(str).str.zfill(5)

# merge
gdf_merged = gdf.merge(
    ecf,
    on="FIPS",
    how="left",
    validate="1:1"  
)

print("Condados en geojson:", len(gdf))

# Guardar el GeoDataFrame resultante como GeoJSON
gdf_merged.to_file("data/processed/counties_ecf_merged.geojson", driver="GeoJSON")