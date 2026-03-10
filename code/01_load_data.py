
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
import requests
import os
import json

def remove_small_islands(geojson):
    for feature in geojson["features"]:
        state = str(feature["properties"].get("STATE", "")).zfill(2)

        if state in ["02", "15"]:
            geom = feature.get("geometry", {})

            if geom.get("type") == "MultiPolygon":
                largest = max(geom["coordinates"], key=lambda poly: len(poly[0]))
                feature["geometry"] = {
                    "type": "Polygon",
                    "coordinates": largest
                }

    return geojson

def load_county_geojson():
    # URL del recurso GeoJSON (Dataset oficial de condados EE.UU.)
    url = "https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json"
    
    # Definición de la ruta de almacenamiento local
    output_path = "data/raw/geojson-counties-fips.json"
    
    # Validación y creación del directorio de destino
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    try:
        # Ejecución de la petición HTTP para la adquisición de datos
        print(f"Descargando recurso desde: {url}")
        response = requests.get(url)
        response.raise_for_status()
        
        # Persistencia del archivo en el sistema de archivos local
       response = requests.get(url)
response.raise_for_status()

counties = response.json()
counties = remove_small_islands(counties)

with open(output_path, "w", encoding="utf-8") as f:
    json.dump(counties, f)
       
        print(f"Proceso finalizado. Archivo guardado en: {output_path}")
        
    except Exception as e:
        print(f"Error en la fase de adquisición de datos: {e}")

if __name__ == "__main__":
    load_county_geojson()

def load_ECF():
    # URL del recurso del csv ECF_total.csv (Dataset oficial de ECF por condado)
    url = "https://github.com/kailingraham/GrahamKnittel_ECF_PNAS_ReplicationMaterials/blob/main/Analysis/overallFootprintCalc/Output/ECF_total.csv"
    
    # Definición de la ruta de almacenamiento local
    output_path = "data/raw/ECF_total.csv"
    
    # Validación y creación del directorio de destino
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    try:
        # Ejecución de la petición HTTP para la adquisición de datos
        print(f"Descargando recurso desde: {url}")
        response = requests.get(url)
        response.raise_for_status()
        
        # Persistencia del archivo en el sistema de archivos local
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(response.text)
        
        print(f"Proceso finalizado. Archivo guardado en: {output_path}")
        
    except Exception as e:
        print(f"Error en la fase de adquisición de datos: {e}")

if __name__ == "__main__":
    load_county_geojson()
