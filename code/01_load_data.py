
"""
01_load_data.py
Carga y limpieza básica de datos del proyecto de replicación.

Tareas:
- Descargar el GeoJSON de condados de EE.UU.
- Eliminar pequeñas islas de Alaska y Hawái
- Descargar el archivo ECF_total.csv
- Guardar ambos archivos en data/raw/
"""

import json
import os
import requests

def remove_small_islands(geojson):
    """
    Para Alaska (02) y Hawaii (15), si la geometría es MultiPolygon,
    conserva solo el polígono principal.
    """
    for feature in geojson["features"]:
        state = str(feature["properties"].get("STATE", "")).zfill(2)

        if state in ["02", "15"]:
            geom = feature.get("geometry", {})

            if geom.get("type") == "MultiPolygon":
                largest = max(geom["coordinates"], key=lambda poly: len(poly[0]))
                feature["geometry"] = {
                    "type": "Polygon",
                    "coordinates": largest,
                }

    return geojson


def load_county_geojson():
    """Descarga el GeoJSON de condados."""
    url = "https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json"
    output_path = "data/raw/geojson-counties-fips.json"

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    print("Downloading county GeoJSON...")

    response = requests.get(url)
    response.raise_for_status()

    counties = response.json()
    counties = remove_small_islands(counties)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(counties, f)

    print("County GeoJSON saved.")


def load_ecf():
    """Descarga el archivo ECF_total.csv."""
    url = "https://raw.githubusercontent.com/kailingraham/GrahamKnittel_ECF_PNAS_ReplicationMaterials/main/Analysis/overallFootprintCalc/Output/ECF_total.csv"
    output_path = "data/raw/ECF_total.csv"

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    print("Downloading ECF dataset...")

    response = requests.get(url)
    response.raise_for_status()

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(response.text)

    print("ECF dataset saved.")


if __name__ == "__main__":
    load_county_geojson()
    load_ecf()
