"""
01_merge_geodata.py
────────────────────────────────────────────────────────────────────────────────
Merges ECF_total.csv with the Plotly GeoJSON of US counties and produces a
GeoDataFrame saved as merged_ecf_counties.geojson (and optionally .parquet).

Inputs
------
  data/raw/ECF_total.csv              output of the ECF calculation notebook
  data/raw/geojson-counties-fips.json US county geometries (Plotly public dataset)

Outputs
-------
  data/processed/merged_ecf_counties.geojson  GeoJSON ready for plotting

Usage
-----
  python 01_merge_geodata.py

Requirements
------------
  pip install pandas geopandas shapely requests
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

# --- MERGE ---
gdf_merged = gdf.merge(
    ecf,
    on="FIPS",
    how="left",
    validate="1:1"  
)

print("Condados en geojson:", len(gdf))

# Guardar si quieres
gdf_merged.to_file("data/processed/counties_ecf_merged.geojson", driver="GeoJSON")