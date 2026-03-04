"""
01_load_data.py
---------------
Carga y validación del archivo ECF_final.csv del repositorio de replicación.

Tareas planificadas:
- Leer ECF_final.csv desde data/raw/
- Inspeccionar estructura: columnas, tipos de datos, valores faltantes
- Validar que el campo de identificación de condado (FIPS) sea consistente
- Exportar resumen descriptivo para verificación

Fuente de datos: https://github.com/kailingraham/GrahamKnittel_ECF_PNAS_ReplicationMaterials
FUENTE: https://github.com/kailingraham/GrahamKnittel_ECF_PNAS_ReplicationMaterials/blob/main/Analysis/overallFootprintCalc/Output/ECF_total.csv
"""

# Geofike
import os
import json
from urllib.request import urlopen

url = "https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json"

with urlopen(url) as response:
    counties = json.load(response)

# Guardar archivo localmente
with open("data/raw/geojson-counties-fips.json", "w", encoding="utf-8") as f:
    json.dump(counties, f)

print("GeoJSON guardado correctamente en data/geojson/")