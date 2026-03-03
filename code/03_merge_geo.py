"""
02_merge_geo.py
---------------
Unión del dataset ECF con la geometría de condados de EE.UU.

Tareas planificadas:
- Cargar shapefile de condados (TIGER/Line, U.S. Census Bureau)
- Unir ECF_final.csv con la geometría usando el código FIPS como llave
- Verificar cobertura: identificar condados sin match
- Exportar GeoDataFrame consolidado a data/processed/

Desafío anticipado: Asegurar que las llaves FIPS del ECF y del shapefile
empaten correctamente (formato, ceros iniciales, etc.)
"""

import pandas as pd
import geopandas as gpd

# --- Rutas  ---
ECF_PATH = r"data/ECF_total.csv"
SHAPE_PATH = r"data/shapes/counties.shp"      # o .geojson / .gpkg